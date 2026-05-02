import os
import sys
from pydantic import ValidationError

# Set PYTHONPATH to current directory
sys.path.append(os.getcwd())

from src.api.v1.endpoints.ssce import SSCEUpdate
from src.api.v1.endpoints.bece import BECEUpdate

def verify_aliases():
    print("Verifying SSCEUpdate alias...")
    try:
        ssce_data = SSCEUpdate.model_validate({"email": "ssce_test@example.com"})
        print(f"SSCE sch_email from 'email' input: {ssce_data.sch_email}")
        assert ssce_data.sch_email == "ssce_test@example.com"
        
        ssce_data_orig = SSCEUpdate.model_validate({"sch_email": "ssce_orig@example.com"})
        print(f"SSCE sch_email from 'sch_email' input: {ssce_data_orig.sch_email}")
        assert ssce_data_orig.sch_email == "ssce_orig@example.com"
    except Exception as e:
        print(f"SSCE verification FAILED: {e}")
        return

    print("\nVerifying BECEUpdate alias...")
    try:
        bece_data = BECEUpdate.model_validate({"email": "bece_test@example.com"})
        print(f"BECE sch_email from 'email' input: {bece_data.sch_email}")
        assert bece_data.sch_email == "bece_test@example.com"
    except Exception as e:
        print(f"BECE verification FAILED: {e}")
        return

    print("\nAll schema aliases verified SUCCESSFUL!")

if __name__ == "__main__":
    verify_aliases()
