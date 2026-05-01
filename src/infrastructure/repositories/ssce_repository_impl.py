from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.ssce.entities import SSCE
from src.domain.ssce.repository import SSCERepository
from src.infrastructure.db.models import SSCEModel

class SQLAlchemySSCERepository(SSCERepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ssce_id: int) -> Optional[SSCE]:
        model = self.db.query(SSCEModel).filter(SSCEModel.id == ssce_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def save(self, ssce: SSCE) -> SSCE:
        model = SSCEModel(
            state_code=ssce.state_code,
            state_name=ssce.state_name,
            sch_num=ssce.sch_num,
            sch_name=ssce.sch_name,
            cust_code=ssce.cust_code,
            cust_name=ssce.cust_name,
            cust_town=ssce.cust_town,
            status=ssce.status,
            type=ssce.type,
            category=ssce.category,
            accd_year=ssce.accd_year,
            lga=ssce.lga
        )
        if ssce.id:
            model.id = ssce.id
            model = self.db.merge(model)
        else:
            self.db.add(model)
        
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[SSCE]:
        models = self.db.query(SSCEModel).offset(skip).limit(limit).all()
        return [self._to_entity(m) for m in models]

    def delete(self, ssce_id: int) -> bool:
        model = self.db.query(SSCEModel).filter(SSCEModel.id == ssce_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    def update(self, ssce_id: int, **kwargs) -> Optional[SSCE]:
        model = self.db.query(SSCEModel).filter(SSCEModel.id == ssce_id).first()
        if not model:
            return None
        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def bulk_create(self, ssce_list: List[SSCE]) -> int:
        models = [
            SSCEModel(
                state_code=ssce.state_code,
                state_name=ssce.state_name,
                sch_num=ssce.sch_num,
                sch_name=ssce.sch_name,
                cust_code=ssce.cust_code,
                cust_name=ssce.cust_name,
                cust_town=ssce.cust_town,
                status=ssce.status,
                type=ssce.type,
                category=ssce.category,
                accd_year=ssce.accd_year,
                lga=ssce.lga
            )
            for ssce in ssce_list
        ]
        self.db.bulk_save_objects(models)
        self.db.commit()
        return len(models)

    def bulk_delete(self, ssce_ids: List[int]) -> int:
        count = self.db.query(SSCEModel).filter(SSCEModel.id.in_(ssce_ids)).delete(synchronize_session=False)
        self.db.commit()
        return count

    def _to_entity(self, model: SSCEModel) -> SSCE:
        return SSCE(
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
