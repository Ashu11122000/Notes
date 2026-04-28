from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base
from datetime import datetime

class Note(Base):
    __tablename__ = "notes"
    
    id: Mapped[int] = mapped_column(primary_key = True, index = True)
    
    title: Mapped[str] = mapped_column(String(255), nullable = False)
    content: Mapped[str] = mapped_column(Text, nullable = False)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable = False)
    created_at: Mapped[datetime] = mapped_column(default = datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default = datetime.utcnow, onupdate = datetime.utcnow)
    
    owner = relationship("User", back_populates= "notes")