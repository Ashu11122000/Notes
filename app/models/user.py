from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True)
    
    email = Column(String, unique = True, index = True, nullable = False)
    
    # Here, nullable is true because Google users won't have password
    hashed_password = Column(String, nullable = True)
    
    is_active = Column(Boolean, default = True)
    
    # Here, role means user/admin
    # By default, it's user
    role = Column(String, default = "user")
    
    # Local or Google
    provider = Column(String, default = "local")
    
    notes = relationship("Note", back_populates = "owner", cascade = "all, delete")
    
    