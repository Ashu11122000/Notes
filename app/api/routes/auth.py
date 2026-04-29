# APIRouter for authentication routes, including email/password and Google OAuth2 login.
# Depends is used to inject the database session and current user information where needed.
# HTTPException is raised for various error conditions, such as invalid credentials or registration issues.
# status is used to set appropriate HTTP status codes for responses.
# Request is used to handle incoming HTTP requests.
from fastapi import APIRouter, Depends, HTTPException, status, Request

# Session is used to interact with the database through SQLAlchemy ORM.
from sqlalchemy.orm import Session

# authlib.integrations.starlette_client is used to handle OAuth2 authentication flows with Google.
# OAuth is configured with client ID and secret, and the appropriate scopes for accessing user information.
from authlib.integrations.starlette_client import OAuth

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.api.deps import get_current_user
from app.core.config import settings
from app.models.user import User

# prefix = "/auth" means all routes in this router will be prefixed with /auth.
# tags = ["Auth"] is used for API documentation grouping in tools like Swagger UI.
# This router will handle all authentication-related endpoints, including registration, login, and Google OAuth2 callbacks.
# OAuth2 callback routes are defined to handle the redirection from Google after authentication, and to create or retrieve user accounts based on the information provided by Google.
router = APIRouter(prefix="/auth", tags=["Auth"])


# OAuth Setup for Google
oauth = OAuth()

# Register the Google OAuth client with the necessary configuration, including client ID, client secret, and server metadata URL for Google's OpenID Connect configuration.
oauth.register(
    name="google",    # Used to reference this OAuth client in the code
    client_id=settings.GOOGLE_CLIENT_ID,    # Client ID obtain from Google Cloud Console
    client_secret=settings.GOOGLE_CLIENT_SECRET,    # Client Secret obtain from Google Cloud Console
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",    # URL to fetch Google's OpenID connect configuration including authorization and token endpoints.
    client_kwargs={    # Additional parameters for the OAuth client, specifying the scope of access requested from the user (email, profile information, etc.)
        "scope": "openid email profile"    # Requesting access to the user's email and profile information as part of the authentication process.
    },
)


# Register a new user with email and password
# This endpoint allows users to create a new account by providing their email and password.
# If the registration is successful, it returns a success message along with the new user's ID.
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = create_user(db, user.email, user.password)

    return {"message": "User registered successfully","user_id": new_user.id}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Use Google login for this account")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": db_user.email, "role": db_user.role})

    return {"access_token": access_token,"token_type": "bearer"}


# Get Current User
@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user


# Google Login Redirect
@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


# Google Callback
@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):

    try:
        token = await oauth.google.authorize_access_token(request)

        # Correct way to extract user info
        user_info = await oauth.google.parse_id_token(request, token)

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Google authentication failed"
        )

    email = user_info.get("email")

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email not found from Google"
        )

    # Check if user exists
    user = get_user_by_email(db, email)

    # Create new Google user if not exists
    if not user:
        user = User(
            email=email,
            provider="google",
            role="user",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # Create JWT
    access_token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }