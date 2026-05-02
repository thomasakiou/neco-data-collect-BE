import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from src.main import app

def test_api():
    client = TestClient(app)
    # Login
    resp = client.post("/api/v1/auth/login", data={"username": "thomas.akiou@gmail.com", "password": "123456"})
    token = resp.json()["access_token"]
    
    # Get first SSCE
    resp = client.get("/api/v1/ssce/", headers={"Authorization": f"Bearer {token}"})
    ssce_id = resp.json()[0]["id"]
    
    # Put request
    payload = {"sch_email": "api_test_sch_email@example.com"}
    print(f"Updating SSCE {ssce_id} with {payload}")
    resp = client.put(f"/api/v1/ssce/{ssce_id}", json=payload, headers={"Authorization": f"Bearer {token}"})
    print(f"Update response: {resp.status_code}")
    print(resp.json())
    
    # Fetch again to verify
    resp = client.get(f"/api/v1/ssce/{ssce_id}", headers={"Authorization": f"Bearer {token}"})
    print(f"Fetch after update: {resp.json().get('sch_email')}")

if __name__ == "__main__":
    test_api()
