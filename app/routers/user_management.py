from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.operation import user_management

router = APIRouter(tags=['User Management'])

get_db = db.get_db

@router.post('/user_management/create_user', status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup)
async def create_users(user: schemas.Reqsignup, db: Session = Depends(get_db)):
    return user_management.create_users(user,db)

@router.get('/user_management/getall_users', response_model=List[schemas.Getsignup])
async def getall_users(db: Session = Depends(get_db)):
    return user_management.getall_users(db)


@router.get('/user_management/getuser_id', response_model=schemas.Getsignup)
async def getuserbyid(admin_id:int,user_id: int, db: Session = Depends(get_db)):
    return user_management.getuser_id(admin_id,user_id, db)

@router.post('/user_management/assign_role', response_model= schemas.Getuser_role)
async def assign_role(user_id: int,role_name: str, db: Session = Depends(get_db)):
    return user_management.assign_role(user_id, role_name, db)

@router.put('/user_management/user_update', response_model=schemas.Getsignup)
async def update_user(user_id: int, data: schemas.Update_user, db: Session = Depends(get_db)):
    return user_management.update_user(user_id, data, db)


@router.delete('/user_management/user_delete')
async def remove(user_id: int, db: Session = Depends(get_db)):
    return user_management.remove(user_id, db)





