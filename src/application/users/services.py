import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import jwt
from passlib.context import CryptContext
from src.core.config import settings
from src.domain.users.entities import User
from src.domain.users.repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def register_user(self, email: str, password: str, state_code: str, state_name: str) -> User:
        hashed_password = self.hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            state_code=state_code,
            state_name=state_name
        )
        return self.user_repo.save(user)

    def change_password(self, user: User, old_password: str, new_password: str) -> bool:
        if not self.verify_password(old_password, user.hashed_password):
            return False
        
        user.hashed_password = self.hash_password(new_password)
        self.user_repo.save(user)
        return True

    def reset_password_for_user(self, email: str) -> Tuple[Optional[str], bool]:
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        
        # Generate random password: 8 characters, letters + digits + special
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        new_password = ''.join(secrets.choice(alphabet) for i in range(12)) # 12 for better security
        
        user.hashed_password = self.hash_password(new_password)
        self.user_repo.save(user)

        # Send email
        from src.infrastructure.services.email_service import EmailService
        email_sent = EmailService.send_reset_password_email(user.email, new_password)
        
        return new_password, email_sent
