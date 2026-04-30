from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.users.entities import User
from src.domain.users.repository import UserRepository
from src.infrastructure.db.models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if not model:
            return None
        return self._to_entity(model)

    def get_by_id(self, user_id: int) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def save(self, user: User) -> User:
        model = UserModel(
            email=user.email,
            state_code=user.state_code,
            state_name=user.state_name,
            hashed_password=user.hashed_password
        )
        if user.id:
            model.id = user.id
            model = self.db.merge(model)
        else:
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def list_by_state(self, state_code: str) -> List[User]:
        models = self.db.query(UserModel).filter(UserModel.state_code == state_code).all()
        return [self._to_entity(m) for m in models]

    def get_all(self) -> List[User]:
        models = self.db.query(UserModel).all()
        return [self._to_entity(m) for m in models]

    def delete(self, user: User) -> None:
        model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if model:
            self.db.delete(model)
            self.db.commit()

    def update(self, user_id: int, **kwargs) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not model:
            return None
        for key, value in kwargs.items():
            if value is not None and hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            state_code=model.state_code,
            state_name=model.state_name,
            hashed_password=model.hashed_password
        )
