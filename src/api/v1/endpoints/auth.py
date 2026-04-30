from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository
from src.application.users.services import AuthService
from src.api.dependencies import get_current_user, get_admin_user
from src.domain.users.entities import User
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    password: str
    state_code: str
    state_name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    state_code: str
    state_name: str

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
    confirm_new_password: str

class PasswordReset(BaseModel):
    email: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    state_code: Optional[str] = None
    state_name: Optional[str] = None

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(repo)
    
    if repo.get_by_email(user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = auth_service.register_user(
        email=user_data.email,
        password=user_data.password,
        state_code=user_data.state_code,
        state_name=user_data.state_name
    )
    
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "state_code": user.state_code, "state_name": user.state_name}
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "state_code": user.state_code,
        "state_name": user.state_name
    }

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(repo)
    
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(
        data={"sub": user.email, "state_code": user.state_code, "state_name": user.state_name}
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "state_code": user.state_code,
        "state_name": user.state_name
    }

@router.post("/change-password")
def change_password(
    data: PasswordChange, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")
    
    repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(repo)
    
    success = auth_service.change_password(current_user, data.old_password, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    return {"message": "Password changed successfully"}

@router.post("/reset-password")
def reset_password(
    data: PasswordReset,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(repo)
    
    new_password, email_sent = auth_service.reset_password_for_user(data.email)
    if not new_password:
        raise HTTPException(status_code=404, detail="User not found")
    
    msg = f"Password reset successfully. New password: {new_password}"
    if email_sent:
        msg += " (Email sent to user)"
    else:
        msg += " (Email sending failed - check SMTP settings)"

    return {
        "message": msg,
        "temp_password": new_password,
        "email_sent": email_sent
    }

@router.get("/users")
def list_users(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    users = repo.get_all()
    return [{"id": u.id, "email": u.email, "state_name": u.state_name, "state_code": u.state_code} for u in users]

@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    auth_service = AuthService(repo)
    
    existing = repo.get_by_id(user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Build update fields
    update_fields = {}
    if data.email is not None:
        # Check email uniqueness
        email_user = repo.get_by_email(data.email)
        if email_user and email_user.id != user_id:
            raise HTTPException(status_code=400, detail="Email already in use by another user")
        update_fields["email"] = data.email
    if data.state_code is not None:
        update_fields["state_code"] = data.state_code
    if data.state_name is not None:
        update_fields["state_name"] = data.state_name
    if data.password is not None:
        update_fields["hashed_password"] = auth_service.hash_password(data.password)
    
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    updated_user = repo.update(user_id, **update_fields)
    return {
        "message": "User updated successfully",
        "user": {
            "id": updated_user.id,
            "email": updated_user.email,
            "state_code": updated_user.state_code,
            "state_name": updated_user.state_name
        }
    }

@router.delete("/users/{email}")
def delete_user(
    email: str,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyUserRepository(db)
    user = repo.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting the super-admin
    if email == "thomas.akiou@gmail.com":
        raise HTTPException(status_code=400, detail="Cannot delete super-admin account")
        
    repo.delete(user)
    return {"message": f"User {email} deleted successfully"}
