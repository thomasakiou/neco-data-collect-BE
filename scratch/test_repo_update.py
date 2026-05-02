import sys
import os
sys.path.append(os.getcwd())

from src.infrastructure.db.session import SessionLocal
from src.infrastructure.repositories.ssce_repository_impl import SQLAlchemySSCERepository
from src.infrastructure.db.models import SSCEModel

def test_repo_update():
    db = SessionLocal()
    try:
        # get any record
        ssce_record = db.query(SSCEModel).first()
        if not ssce_record:
            print("No record found")
            return
            
        ssce_id = ssce_record.id
        old_email = ssce_record.sch_email
        print(f"Record {ssce_id} old email: {old_email}")
        
        repo = SQLAlchemySSCERepository(db)
        # Try to update
        updated_entity = repo.update(ssce_id, sch_email="update_via_repo@test.com")
        
        print(f"Returned entity sch_email: {updated_entity.sch_email}")
        
        # Verify in fresh db session
    finally:
        db.close()
        
    db_fresh = SessionLocal()
    try:
        fresh_record = db_fresh.query(SSCEModel).filter(SSCEModel.id == ssce_id).first()
        print(f"Fresh DB fetch sch_email: {fresh_record.sch_email}")
    finally:
        db_fresh.close()

if __name__ == "__main__":
    test_repo_update()
