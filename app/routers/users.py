# from app.database import db
# from fastapi import APIRouter, Request, status, Depends, HTTPException
# from app import schemas
# from sqlalchemy.orm.session import Session
# from typing import List
# from app.operation import users

# router = APIRouter()

# get_db = db.get_db


# @router.get('/token_based_user_verfy')
# def get_user(request: Request,db: Session = Depends(get_db)):
#     return users.get_user(request, db)