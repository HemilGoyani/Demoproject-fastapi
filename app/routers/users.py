from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Usersignup
from app.operation import users

router = APIRouter(tags=['User'])

get_db = db.get_db

@router.post('/user/registration', status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup)
async def create(user: schemas.Reqsignup, db: Session = Depends(get_db)):
    return users.create(user, db)


@router.get('/user/signin', response_model=schemas.Getsignup)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    return users.login(email,password,db)

@router.patch('/user/login', response_model=schemas.Getsignup)
async def login(user: schemas.login, db: Session = Depends(get_db)):
    return users.login2(user,db)


@router.get('/user/forgot_password')
async def forgotpass(id: int, email:str,db: Session = Depends(get_db)):
    return users.forgotpass(id, email, db)


@router.put('/user/change_pass',status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup)
async def changepass(id: int, oldpassword:str, newpassword:str,confirm_new_password:str, db: Session = Depends(get_db)):
    return users.changepass(id,oldpassword, newpassword, confirm_new_password, db)


