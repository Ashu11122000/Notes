from sqlalchemy import Boolean, Column, Integer, String # type: ignore
from sqlalchemy.orm import relationship # type: ignore

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    role = Column(
        String(50),
        default="user",
        nullable=False
    )

    # Relationships
    notes = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete-orphan"
    )