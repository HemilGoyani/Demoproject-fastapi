from app.database import db
from fastapi import APIRouter,status, Depends
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import modules
from typing import List


router = APIRouter(prefix='/module',tags=["Modules"])
get_db = db.get_db

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getmodule)
async def create_module(module_name:str , db: Session = Depends(get_db)):
    return modules.create_module(module_name, db)


@router.get('/getall', status_code=status.HTTP_201_CREATED, response_model=List[schemas.Getmodule])
async def get_module(db: Session = Depends(get_db)):
    return modules.get_module(db)

@router.delete('/delete/{module_id}')    
async def delete_module(module_id: int,db: Session = Depends(get_db)):
    return modules.delete_module(module_id,db)
