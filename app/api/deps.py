from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import Session
from app.services.user_service import get_user_by_email
from app.core.security import decode_access_token

# OAuth2 scheme which reads Bearer token from header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "/auth/login")

# Get current user using JWT Authentication
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Expired token")
    
    email: str = payload.get("sub")
    
    if email is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Token payload invalid")
    
    user = get_user_by_email(db, email)
    
    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")
    
    return user

# Role-based Access Control for single role
def required_role(required_role: str):
    
    def role_checker(current_user = Depends(get_current_user)):
        
        if current_user.role != required_role:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "You do not have permission to perform this action")
        
        return current_user
    
    return role_checker

# Role-Based Access Control for multiple roles
def require_roles(roles: list):
    
    def role_checker(current_user = Depends(get_current_user)):
        
        if current_user.role not in roles:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Access Denied")
        
        return current_user
    
    return role_checker
