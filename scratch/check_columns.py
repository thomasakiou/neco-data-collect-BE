from src.infrastructure.db.session import SessionLocal
from src.infrastructure.db.models import SSCEModel
from sqlalchemy import inspect

db = SessionLocal()
try:
    inst = inspect(SSCEModel)
    columns = [c_attr.key for c_attr in inst.mapper.column_attrs]
    print(f"Columns in SSCEModel: {columns}")
finally:
    db.close()
