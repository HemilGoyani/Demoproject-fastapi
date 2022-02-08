import fastapi
from app.database import db
from fastapi import APIRouter, FastAPI, status, Depends
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import modules
from typing import List
from middleware.security import check_token_valid


router = APIRouter(tags=["Modules"])
get_db = db.get_db

@router.post('/module/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getmodule)
async def create_module(module_name:str , db: Session = Depends(get_db)):
    return modules.create_module(module_name, db)


@router.get('/module/getall', status_code=status.HTTP_201_CREATED, response_model=List[schemas.Getmodule])
async def get_module(db: Session = Depends(get_db)):
    return modules.get_module(db)

@router.delete('/module/delete')    
async def delete_module(module_id: int,db: Session = Depends(get_db)):
    return modules.delete_module(module_id,db)
