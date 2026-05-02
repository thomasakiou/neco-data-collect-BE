import sys
import os
sys.path.append(os.getcwd())

from src.api.v1.endpoints.ssce import SSCEUpdate
from src.infrastructure.db.models import SSCEModel

update_obj = SSCEUpdate(sch_email="test@test.com")
dump = update_obj.model_dump(exclude_none=True)
print("Dumped dict:", dump)

model = SSCEModel()
for k, v in dump.items():
    if hasattr(model, k):
        setattr(model, k, v)
        print(f"Set {k} to {v}")
    else:
        print(f"Model has no attribute {k}")
print("Final model sch_email:", model.sch_email)
