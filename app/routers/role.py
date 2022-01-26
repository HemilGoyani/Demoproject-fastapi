from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import role
from typing import List

router = APIRouter(tags=["Roles"])

get_db = db.get_db


@router.post('/role/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getroles)
async def create_role( name: str, active: bool, db: Session = Depends(get_db)):
    return role.create_role(name, active, db)

@router.get('/role/geta_ll', status_code=status.HTTP_201_CREATED, response_model=List[schemas.Getroles])
async def create_role(db: Session = Depends(get_db)):
    return role.get_role(db)

@router.delete('/role/delete')    
async def delete_role(role_id: int,db: Session = Depends(get_db)):
    return role.delete_role(role_id,db)