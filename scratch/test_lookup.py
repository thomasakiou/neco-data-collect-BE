import sys
import os

# Add src to sys.path
sys.path.append(os.getcwd())

from src.infrastructure.db.session import SessionLocal
from src.infrastructure.repositories.ssce_repository_impl import SQLAlchemySSCERepository
from src.domain.ssce.entities import SSCE

def test_lga_lookup():
    db = SessionLocal()
    repo = SQLAlchemySSCERepository(db)
    
    # Test creating a record with lga name but no lga_code
    # Abia (001), Aba North (should be 001001)
    test_ssce = SSCE(
        state_code="001",
        state_name="Abia",
        sch_num="TEST001",
        sch_name="Test School",
        cust_code="C001",
        cust_name="Test Cust",
        cust_town="Test Town",
        lga="Aba North" # No lga_code provided
    )
    
    print(f"Creating SSCE record for LGA: {test_ssce.lga}...")
    saved = repo.save(test_ssce)
    print(f"Saved Record ID: {saved.id}")
    print(f"Saved LGA Code: {saved.lga_code}")
    
    if saved.lga_code == "001001":
        print("Success! lga_code was automatically fetched.")
    else:
        print(f"Failure. lga_code is {saved.lga_code}, expected 001001.")
    
    # Cleanup
    repo.delete(saved.id)
    db.close()

if __name__ == "__main__":
    test_lga_lookup()
