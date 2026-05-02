import urllib.request
import urllib.parse
import json

def test_running_api_empty_string():
    base_url = "http://localhost:8010/api/v1"
    
    # Login
    data = urllib.parse.urlencode({"username": "thomas.akiou@gmail.com", "password": "123456"}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/auth/login", data=data)
    with urllib.request.urlopen(req) as response:
        token = json.loads(response.read().decode())["access_token"]
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Get SSCE
    req = urllib.request.Request(f"{base_url}/ssce/", headers=headers)
    with urllib.request.urlopen(req) as response:
        ssce_id = json.loads(response.read().decode())[0]["id"]
        
    # 1. Update with a value
    payload = json.dumps({"sch_email": "hello@world.com"}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/ssce/{ssce_id}", data=payload, headers=headers, method="PUT")
    with urllib.request.urlopen(req) as response:
        pass
        
    # 2. Update with empty string
    payload = json.dumps({"sch_email": ""}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/ssce/{ssce_id}", data=payload, headers=headers, method="PUT")
    with urllib.request.urlopen(req) as response:
        pass

    # Fetch SSCE again
    req = urllib.request.Request(f"{base_url}/ssce/{ssce_id}", headers=headers)
    with urllib.request.urlopen(req) as response:
        sch_email = json.loads(response.read().decode())["sch_email"]
        print(f"Fetch after empty string update sch_email: '{sch_email}'")

if __name__ == "__main__":
    test_running_api_empty_string()
