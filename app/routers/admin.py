from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Usersignup
from app.operation import admin

router = APIRouter(tags=['Admin'])

get_db = db.get_db


@router.get('/user/all', response_model=List[schemas.Getsignup])
async def getallusers(db: Session = Depends(get_db)):
    return admin.getallusers(db)


@router.get('/user/id', response_model=schemas.Getsignup)
async def getuserbyid(id: int, db: Session = Depends(get_db)):
    return admin.getuserbyid(id, db)


@router.put('/user/update', response_model=schemas.Getsignup)
async def update_user(id: int, data: schemas.Update_user, db: Session = Depends(get_db)):
    return admin.update_user(id, data, db)


@router.delete('/user/delete')
async def remove(id: int, db: Session = Depends(get_db)):
    return admin.remove(id, db)

