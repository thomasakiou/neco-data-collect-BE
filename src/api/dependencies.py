from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.core.config import settings
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository
from src.domain.users.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    repo = SQLAlchemyUserRepository(db)
    user = repo.get_by_email(email)
    if user is None:
        raise credentials_exception
    return user

def get_state_code(current_user: User = Depends(get_current_user)) -> str:
    """
    Dependency to get the state_code of the current logged in user.
    Use this in other endpoints to filter data.
    """
    return current_user.state_code

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency that ensures the current user is an admin (state_code '000').
    Raises 403 Forbidden if not.
    """
    if current_user.state_code != "000":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
