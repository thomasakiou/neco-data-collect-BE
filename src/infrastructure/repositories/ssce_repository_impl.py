from typing import Optional, List
from sqlalchemy.orm import Session
from src.domain.ssce.entities import SSCE
from src.domain.ssce.repository import SSCERepository
from src.infrastructure.db.models import SSCEModel, LGAModel

class SQLAlchemySSCERepository(SSCERepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ssce_id: int) -> Optional[SSCE]:
        model = self.db.query(SSCEModel).filter(SSCEModel.id == ssce_id).first()
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

    def save(self, ssce: SSCE) -> SSCE:
        lga_code = ssce.lga_code
        if not lga_code and ssce.lga:
            lga_code = self._get_lga_code(ssce.lga, ssce.state_code)

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
            lga=ssce.lga,
            sch_email=ssce.sch_email,
            accreditation_type=ssce.accreditation_type,
            lga_code=lga_code
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

    def bulk_create(self, ssce_list: List[SSCE]) -> int:
        # Pre-fetch relevant LGA codes to minimize queries
        unique_lga_state_pairs = set()
        for ssce in ssce_list:
            if not ssce.lga_code and ssce.lga:
                unique_lga_state_pairs.add((ssce.lga, ssce.state_code))
        
        lga_code_map = {}
        if unique_lga_state_pairs:
            # This is a bit complex for a single query with multiple pairs, 
            # so we'll just do a few queries or one query and filter in memory if the set is small.
            # For now, let's just do individual lookups or a simpler batch if possible.
            # Given typically records are from one state or a few, we can optimize.
            for lga_name, state_code in unique_lga_state_pairs:
                lga_code_map[(lga_name, state_code)] = self._get_lga_code(lga_name, state_code)

        models = []
        for ssce in ssce_list:
            lga_code = ssce.lga_code
            if not lga_code and ssce.lga:
                lga_code = lga_code_map.get((ssce.lga, ssce.state_code))

            models.append(SSCEModel(
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
                lga=ssce.lga,
                sch_email=ssce.sch_email,
                accreditation_type=ssce.accreditation_type,
                lga_code=lga_code
            ))
        
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
            lga=model.lga,
            sch_email=model.sch_email,
            accreditation_type=model.accreditation_type,
            lga_code=model.lga_code
        )
