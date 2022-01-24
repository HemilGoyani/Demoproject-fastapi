from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Usersignup
from app.operation import crud
import re
router = APIRouter()

get_db = db.get_db

@router.post('/user/registration', status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup,tags=["User"])
async def create(user: schemas.Reqsignup, db: Session = Depends(get_db)):
    return crud.create(user, db)


@router.get('/user/signin', response_model=schemas.Getsignup, tags=['User'])
async def login(email: str, password: str, db: Session = Depends(get_db)):
    return crud.login(email,password,db)

@router.patch('/user/login', response_model=schemas.Getsignup, tags=['User'])
async def login(user: schemas.login, db: Session = Depends(get_db)):
    return crud.login2(user,db)



@router.get('/user/forgot_password',tags=['User'])
async def forgotpass(id: int, email:str,db: Session = Depends(get_db)):
    return crud.forgotpass(id, email, db)


@router.put('/user/change_pass',status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup,tags=["User"])
async def changepass(id: int, oldpassword:str, newpassword:str,confirm_new_password:str, db: Session = Depends(get_db)):
    return crud.changepass(id,oldpassword, newpassword, confirm_new_password, db)


@router.get('/user/all', response_model=List[schemas.Getsignup], tags=['Admin'])
async def getallusers(db: Session = Depends(get_db)):
    return crud.getallusers(db)


@router.get('/user/id', response_model=schemas.Getsignup, tags=['Admin'])
async def getuserbyid(id: int, db: Session = Depends(get_db)):
    return crud.getuserbyid(id, db)


@router.put('/user/update', response_model=schemas.Getsignup, tags=['Admin'])
async def update_user(id: int, data: schemas.Update_user, db: Session = Depends(get_db)):
    return crud.update_user(id, data, db)


@router.delete('/user/delete', tags=['Admin'])
async def remove(id: int, db: Session = Depends(get_db)):
    return crud.remove(id, db)
