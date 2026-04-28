from pydantic import BaseModel, EmailStr

# Class for user register
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
# Class for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# Class for response schema which never exposes password
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    
    class Config:
        from_attributes = True