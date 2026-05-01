import csv
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.ssce_repository_impl import SQLAlchemySSCERepository
from src.domain.ssce.entities import SSCE
from src.api.dependencies import get_current_user
from src.domain.users.entities import User

router = APIRouter()

class SSCEBase(BaseModel):
    state_code: str
    state_name: str
    sch_num: str
    sch_name: str
    cust_code: str
    cust_name: str
    cust_town: str
    status: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    accd_year: Optional[str] = None
    lga: Optional[str] = None

class SSCECreate(SSCEBase):
    pass

class SSCEUpdate(BaseModel):
    state_code: Optional[str] = None
    state_name: Optional[str] = None
    sch_num: Optional[str] = None
    sch_name: Optional[str] = None
    cust_code: Optional[str] = None
    cust_name: Optional[str] = None
    cust_town: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    accd_year: Optional[str] = None
    lga: Optional[str] = None

class SSCEResponse(SSCEBase):
    id: int
    class Config:
        from_attributes = True

class BulkDeleteRequest(BaseModel):
    ids: List[int]

@router.post("/", response_model=SSCEResponse, status_code=status.HTTP_201_CREATED)
def create_ssce(
    data: SSCECreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemySSCERepository(db)
    entity = SSCE(**data.model_dump())
    return repo.save(entity)

@router.get("/", response_model=List[SSCEResponse])
def list_ssce(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemySSCERepository(db)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{ssce_id}", response_model=SSCEResponse)
def get_ssce(
    ssce_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemySSCERepository(db)
    entity = repo.get_by_id(ssce_id)
    if not entity:
        raise HTTPException(status_code=404, detail="SSCE record not found")
    return entity

@router.put("/{ssce_id}", response_model=SSCEResponse)
def update_ssce(
    ssce_id: int, 
    data: SSCEUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemySSCERepository(db)
    updated = repo.update(ssce_id, **data.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="SSCE record not found")
    return updated

@router.delete("/{ssce_id}")
def delete_ssce(
    ssce_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemySSCERepository(db)
    if not repo.delete(ssce_id):
        raise HTTPException(status_code=404, detail="SSCE record not found")
    return {"message": "SSCE record deleted successfully"}

@router.post("/upload")
async def upload_ssce(
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
    
    ssce_list = []
    for row in reader:
        ssce_list.append(SSCE(
            state_code=row.get('state_code'),
            state_name=row.get('state_name'),
            sch_num=row.get('sch_num'),
            sch_name=row.get('sch_name'),
            cust_code=row.get('cust_code'),
            cust_name=row.get('cust_name'),
            cust_town=row.get('cust_town'),
            status=row.get('status'),
            type=row.get('type'),
            category=row.get('category'),
            accd_year=row.get('accd_year'),
            lga=row.get('lga')
        ))
    
    repo = SQLAlchemySSCERepository(db)
    count = repo.bulk_create(ssce_list)
    return {"message": f"Successfully imported {count} SSCE records"}

@router.post("/bulk-delete")
def bulk_delete_ssce(
    request: BulkDeleteRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemySSCERepository(db)
    count = repo.bulk_delete(request.ids)
    return {"message": f"Successfully deleted {count} SSCE records"}
