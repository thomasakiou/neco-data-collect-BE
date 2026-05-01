import csv
import sys
import os

# Add src to sys.path
sys.path.append(os.getcwd())

from src.infrastructure.db.session import SessionLocal
from src.infrastructure.repositories.lga_repository_impl import SQLAlchemyLGARepository
from src.domain.lga.entities import LGA

def seed_lgas():
    db = SessionLocal()
    repo = SQLAlchemyLGARepository(db)
    
    csv_path = 'nigeria_lgas.csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        return

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        lga_list = []
        for row in reader:
            lga_list.append(LGA(
                state_name=row['State'],
                state_code=row['state_code'],
                lga_name=row['LGA']
            ))
    
    if lga_list:
        count = repo.bulk_create(lga_list)
        print(f"Successfully seeded {count} LGA records")
    else:
        print("No records found in CSV")
    
    db.close()

if __name__ == "__main__":
    seed_lgas()
