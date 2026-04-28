from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password

# Service logic for creating user or register user
def create_user(db: Session, email: str, password: str) -> User:
    new_user = User(email = email, hashed_password = hash_password(password), role = "user", provider = "local")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# Service logic for getting user by email used in login + Google auth
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

# Service logic for getting user by id
def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

# Service logic for creating google user (no password)
def create_user_by_google(db: Session, email: str) -> User:
    user = User(email = email, provider = "google", role="user")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user