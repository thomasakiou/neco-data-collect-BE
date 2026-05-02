import urllib.request
import urllib.parse
import json

def test_running_api():
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
        
    # Update SSCE
    payload = json.dumps({"sch_email": "real_api_test@example.com"}).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/ssce/{ssce_id}", data=payload, headers=headers, method="PUT")
    
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Update response: {response.status}")
            print(json.loads(response.read().decode()))
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} {e.reason}")
        print(e.read().decode())

    # Get SSCE again
    req = urllib.request.Request(f"{base_url}/ssce/{ssce_id}", headers=headers)
    with urllib.request.urlopen(req) as response:
        sch_email = json.loads(response.read().decode())["sch_email"]
        print(f"Fetch after update sch_email: {sch_email}")

if __name__ == "__main__":
    test_running_api()
