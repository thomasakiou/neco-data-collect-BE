import csv
import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from src.infrastructure.db.session import get_db
from src.infrastructure.repositories.bece_repository_impl import SQLAlchemyBECERepository
from src.domain.bece.entities import BECE
from src.api.dependencies import get_current_user
from src.domain.users.entities import User

router = APIRouter()

class BECEBase(BaseModel):
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

class BECECreate(BECEBase):
    pass

class BECEUpdate(BaseModel):
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

class BECEResponse(BECEBase):
    id: int
    class Config:
        from_attributes = True

class BulkDeleteRequest(BaseModel):
    ids: List[int]

@router.post("/", response_model=BECEResponse, status_code=status.HTTP_201_CREATED)
def create_bece(
    data: BECECreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyBECERepository(db)
    entity = BECE(**data.model_dump())
    return repo.save(entity)

@router.get("/", response_model=List[BECEResponse])
def list_bece(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyBECERepository(db)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{bece_id}", response_model=BECEResponse)
def get_bece(
    bece_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyBECERepository(db)
    entity = repo.get_by_id(bece_id)
    if not entity:
        raise HTTPException(status_code=404, detail="BECE record not found")
    return entity

@router.put("/{bece_id}", response_model=BECEResponse)
def update_bece(
    bece_id: int, 
    data: BECEUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyBECERepository(db)
    updated = repo.update(bece_id, **data.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="BECE record not found")
    return updated

@router.delete("/{bece_id}")
def delete_bece(
    bece_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyBECERepository(db)
    if not repo.delete(bece_id):
        raise HTTPException(status_code=404, detail="BECE record not found")
    return {"message": "BECE record deleted successfully"}

@router.post("/upload")
async def upload_bece(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.DictReader(io.StringIO(decoded))
    
    bece_list = []
    for row in reader:
        bece_list.append(BECE(
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
    
    repo = SQLAlchemyBECERepository(db)
    count = repo.bulk_create(bece_list)
    return {"message": f"Successfully imported {count} BECE records"}

@router.post("/bulk-delete")
def bulk_delete_bece(
    request: BulkDeleteRequest, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    repo = SQLAlchemyBECERepository(db)
    count = repo.bulk_delete(request.ids)
    return {"message": f"Successfully deleted {count} BECE records"}
