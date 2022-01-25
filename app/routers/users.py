from app.database import db
from fastapi import APIRouter, Request, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.operation import users,admin

router = APIRouter(tags=['User'])

get_db = db.get_db


@router.post('/user/signin', response_model=schemas.Getsignup)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    return users.login(email,password,db)


@router.post('/user/forgot_password/sent_email')
async def forgot_paswords(request: Request,user_id: int, email:str,db: Session = Depends(get_db)):
    return users.forgot_paswords_email_sent(user_id, email, db)


@router.put('/user/change_password',status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup)
async def change_password(id: int, oldpassword:str, newpassword:str,confirm_new_password:str, db: Session = Depends(get_db)):
    return users.change_password(id,oldpassword, newpassword, confirm_new_password, db)


