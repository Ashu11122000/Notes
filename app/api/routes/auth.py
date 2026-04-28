from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.user_service import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# Register
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = create_user(db, user.email, user.password)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# Login
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = get_user_by_email(db, user.email)

    # User not found
    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    # Google user trying password login
    if not db_user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Use Google login for this account"
        )

    # Password check (THIS WAS MISSING)
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

    # Create JWT with role
    access_token = create_access_token({
        "sub": db_user.email,
        "role": db_user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# Get Current User
@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user