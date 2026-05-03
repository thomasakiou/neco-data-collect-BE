from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.lga.entities import LGA
from src.domain.lga.repository import LGARepository
from src.infrastructure.db.models import LGAModel

class SQLAlchemyLGARepository(LGARepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, lga_id: int) -> Optional[LGA]:
        model = self.db.query(LGAModel).filter(LGAModel.id == lga_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def save(self, lga: LGA) -> LGA:
        model = LGAModel(
            state_name=lga.state_name,
            state_code=lga.state_code,
            lga_name=lga.lga_name,
            lga_code=lga.lga_code
        )
        if lga.id:
            model.id = lga.id
            model = self.db.merge(model)
        else:
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[LGA]:
        models = self.db.query(LGAModel).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models]

    def delete(self, lga_id: int) -> bool:
        model = self.db.query(LGAModel).filter(LGAModel.id == lga_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def update(self, lga_id: int, **kwargs) -> Optional[LGA]:
        model = self.db.query(LGAModel).filter(LGAModel.id == lga_id).first()
        if not model:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def bulk_create(self, lga_list: List[LGA]) -> int:
        models = [
            LGAModel(
                state_name=lga.state_name,
                state_code=lga.state_code,
                lga_name=lga.lga_name,
                lga_code=lga.lga_code
            )
            for lga in lga_list
        ]
        self.db.bulk_save_objects(models)
        self.db.commit()
        return len(models)

    def bulk_delete(self, lga_ids: List[int]) -> int:
        count = self.db.query(LGAModel).filter(LGAModel.id.in_(lga_ids)).delete(synchronize_session=False)
        self.db.commit()
        return count

    def _to_entity(self, model: LGAModel) -> LGA:
        return LGA(
            id=model.id,
            state_name=model.state_name,
            state_code=model.state_code,
            lga_name=model.lga_name,
            lga_code=model.lga_code
        )
