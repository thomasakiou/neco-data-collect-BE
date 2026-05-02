import os
import sys
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.main import app
from src.infrastructure.db.session import SessionLocal
from src.infrastructure.db.models import SSCEModel

# Set PYTHONPATH to current directory
sys.path.append(os.getcwd())

client = TestClient(app)

def test_email_alias():
    # 1. Login to get token
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "thomas.akiou@gmail.com", "password": "123456"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Get an existing SSCE record ID
    db = SessionLocal()
    ssce_record = db.query(SSCEModel).first()
    if not ssce_record:
        print("No SSCE records found in database. Skipping test.")
        db.close()
        return
    
    ssce_id = ssce_record.id
    db.close()

    # 3. Update using 'email' field instead of 'sch_email'
    test_email = "updated_via_alias@test.com"
    update_payload = {"email": test_email}
    
    print(f"Updating SSCE {ssce_id} with payload: {update_payload}")
    response = client.put(
        f"/api/v1/ssce/{ssce_id}",
        json=update_payload,
        headers=headers
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["sch_email"] == test_email

    # 4. Verify in database
    db = SessionLocal()
    updated_record = db.query(SSCEModel).filter(SSCEModel.id == ssce_id).first()
    print(f"DB sch_email: {updated_record.sch_email}")
    assert updated_record.sch_email == test_email
    db.close()
    
    print("Verification SUCCESSFUL!")

if __name__ == "__main__":
    test_email_alias()
