from sqlalchemy.orm import Session # type: ignore

from app.core.security import hash_password
from app.models.user import User


# Create User
def create_user(
    db: Session,
    email: str,
    password: str
) -> User:

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role="user",
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# Get User By Email
def get_user_by_email(
    db: Session,
    email: str
) -> User | None:

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# Get User By ID
def get_user_by_id(
    db: Session,
    user_id: int
) -> User | None:

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )