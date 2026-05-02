import sys
import os
sys.path.append(os.getcwd())

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_api():
    # Login
    resp = client.post("/api/v1/auth/login", data={"username": "thomas.akiou@gmail.com", "password": "123456"})
    token = resp.json()["access_token"]
    
    # Get first SSCE
    resp = client.get("/api/v1/ssce/", headers={"Authorization": f"Bearer {token}"})
    ssce_id = resp.json()[0]["id"]
    
    # Put request
    payload = {"sch_email": "real_api_test@example.com"}
    resp = client.put(f"/api/v1/ssce/{ssce_id}", json=payload, headers={"Authorization": f"Bearer {token}"})
    print(resp.json())

if __name__ == "__main__":
    test_api()
