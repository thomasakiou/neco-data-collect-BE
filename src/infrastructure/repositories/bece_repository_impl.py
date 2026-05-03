from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.bece.entities import BECE
from src.domain.bece.repository import BECERepository
from src.infrastructure.db.models import BECEModel, LGAModel

class SQLAlchemyBECERepository(BECERepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, bece_id: int) -> Optional[BECE]:
        model = self.db.query(BECEModel).filter(BECEModel.id == bece_id).first()
        if not model:
            return None
        return self._to_entity(model)

    def _get_lga_code(self, lga_name: str, state_code: str) -> Optional[str]:
        if not lga_name:
            return None
        lga_record = self.db.query(LGAModel).filter(
            LGAModel.lga_name == lga_name,
            LGAModel.state_code == state_code
        ).first()
        return lga_record.lga_code if lga_record else None

    def save(self, bece: BECE) -> BECE:
        lga_code = bece.lga_code
        if not lga_code and bece.lga:
            lga_code = self._get_lga_code(bece.lga, bece.state_code)

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
            lga=bece.lga,
            sch_email=bece.sch_email,
            accreditation_type=bece.accreditation_type,
            lga_code=lga_code
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
        
        # If lga is being updated but lga_code is not provided, fetch it
        if 'lga' in kwargs and not kwargs.get('lga_code'):
            state_code = kwargs.get('state_code') or model.state_code
            kwargs['lga_code'] = self._get_lga_code(kwargs['lga'], state_code)

        for key, value in kwargs.items():
            if hasattr(model, key):
                setattr(model, key, value)
        self.db.commit()
        self.db.refresh(model)
        return self._to_entity(model)

    def bulk_create(self, bece_list: List[BECE]) -> int:
        # Pre-fetch relevant LGA codes to minimize queries
        unique_lga_state_pairs = set()
        for bece in bece_list:
            if not bece.lga_code and bece.lga:
                unique_lga_state_pairs.add((bece.lga, bece.state_code))
        
        lga_code_map = {}
        if unique_lga_state_pairs:
            for lga_name, state_code in unique_lga_state_pairs:
                lga_code_map[(lga_name, state_code)] = self._get_lga_code(lga_name, state_code)

        models = []
        for bece in bece_list:
            lga_code = bece.lga_code
            if not lga_code and bece.lga:
                lga_code = lga_code_map.get((bece.lga, bece.state_code))

            models.append(BECEModel(
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
                lga=bece.lga,
                sch_email=bece.sch_email,
                accreditation_type=bece.accreditation_type,
                lga_code=lga_code
            ))
        
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
            lga=model.lga,
            sch_email=model.sch_email,
            accreditation_type=model.accreditation_type,
            lga_code=model.lga_code
        )
