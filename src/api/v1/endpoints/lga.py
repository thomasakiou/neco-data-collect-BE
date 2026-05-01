import csv
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.lga_repository_impl import SQLAlchemyLGARepository
from src.domain.lga.entities import LGA
from src.api.dependencies import get_current_user
from src.domain.users.entities import User

router = APIRouter()

class LGABase(BaseModel):
    state_name: str
    state_code: str
    lga_name: str

class LGACreate(LGABase):
    pass

class LGAUpdate(BaseModel):
    state_name: Optional[str] = None
    state_code: Optional[str] = None
    lga_name: Optional[str] = None

class LGAResponse(LGABase):
    id: int
    class Config:
        from_attributes = True

class BulkDeleteRequest(BaseModel):
    ids: List[int]

@router.post("/", response_model=LGAResponse, status_code=status.HTTP_201_CREATED)
def create_lga(
    data: LGACreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyLGARepository(db)
    entity = LGA(**data.model_dump())
    return repo.save(entity)

@router.get("/", response_model=List[LGAResponse])
def list_lgas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyLGARepository(db)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{lga_id}", response_model=LGAResponse)
def get_lga(
    lga_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyLGARepository(db)
    entity = repo.get_by_id(lga_id)
    if not entity:
        raise HTTPException(status_code=404, detail="LGA record not found")
    return entity

@router.put("/{lga_id}", response_model=LGAResponse)
def update_lga(
    lga_id: int, 
    data: LGAUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyLGARepository(db)
    updated = repo.update(lga_id, **data.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="LGA record not found")
    return updated

@router.delete("/{lga_id}")
def delete_lga(
    lga_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyLGARepository(db)
    if not repo.delete(lga_id):
        raise HTTPException(status_code=404, detail="LGA record not found")
    return {"message": "LGA record deleted successfully"}

@router.post("/upload")
async def upload_lgas(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    try:
        decoded = content.decode('utf-8')
    except UnicodeDecodeError:
        decoded = content.decode('latin-1')
    
    reader = csv.DictReader(io.StringIO(decoded))
    
    lga_list = []
    for row in reader:
        # Map CSV headers to model fields
        # nigeria_lgas.csv has: State,state_code,LGA
        lga_list.append(LGA(
            state_name=row.get('State') or row.get('state_name'),
            state_code=row.get('state_code'),
            lga_name=row.get('LGA') or row.get('lga_name')
        ))
    
    if not lga_list:
        raise HTTPException(status_code=400, detail="No valid data found in CSV")

    repo = SQLAlchemyLGARepository(db)
    count = repo.bulk_create(lga_list)
    return {"message": f"Successfully imported {count} LGA records"}

@router.post("/bulk-delete")
def bulk_delete_lgas(
    request: BulkDeleteRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyLGARepository(db)
    count = repo.bulk_delete(request.ids)
    return {"message": f"Successfully deleted {count} LGA records"}
