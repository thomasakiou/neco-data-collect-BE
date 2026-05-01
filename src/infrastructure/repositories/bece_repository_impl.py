from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.bece.entities import BECE
from src.domain.bece.repository import BECERepository
from src.infrastructure.db.models import BECEModel

class SQLAlchemyBECERepository(BECERepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, bece_id: int) -> Optional[BECE]:
        model = self.db.query(BECEModel).filter(BECEModel.id == bece_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def save(self, bece: BECE) -> BECE:
        model = BECEModel(
            state_code=bece.state_code,
            state_name=bece.state_name,
            sch_num=bece.sch_num,
            sch_name=bece.sch_name,
            cust_code=bece.cust_code,
            cust_name=bece.cust_name,
            cust_town=bece.cust_town,
            status=bece.status,
            type=bece.type,
            category=bece.category,
            accd_year=bece.accd_year,
            lga=bece.lga
        )
        if bece.id:
            model.id = bece.id
            model = self.db.merge(model)
        else:
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[BECE]:
        models = self.db.query(BECEModel).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models]

    def delete(self, bece_id: int) -> bool:
        model = self.db.query(BECEModel).filter(BECEModel.id == bece_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def update(self, bece_id: int, **kwargs) -> Optional[BECE]:
        model = self.db.query(BECEModel).filter(BECEModel.id == bece_id).first()
        if not model:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def bulk_create(self, bece_list: List[BECE]) -> int:
        models = [
            BECEModel(
                state_code=bece.state_code,
                state_name=bece.state_name,
                sch_num=bece.sch_num,
                sch_name=bece.sch_name,
                cust_code=bece.cust_code,
                cust_name=bece.cust_name,
                cust_town=bece.cust_town,
                status=bece.status,
                type=bece.type,
                category=bece.category,
                accd_year=bece.accd_year,
                lga=bece.lga
            )
            for bece in bece_list
        ]
        self.db.bulk_save_objects(models)
        self.db.commit()
        return len(models)

    def bulk_delete(self, bece_ids: List[int]) -> int:
        count = self.db.query(BECEModel).filter(BECEModel.id.in_(bece_ids)).delete(synchronize_session=False)
        self.db.commit()
        return count

    def _to_entity(self, model: BECEModel) -> BECE:
        return BECE(
            id=model.id,
            state_code=model.state_code,
            state_name=model.state_name,
            sch_num=model.sch_num,
            sch_name=model.sch_name,
            cust_code=model.cust_code,
            cust_name=model.cust_name,
            cust_town=model.cust_town,
            status=model.status,
            type=model.type,
            category=model.category,
            accd_year=model.accd_year,
            lga=model.lga
        )
