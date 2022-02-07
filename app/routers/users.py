from app.database import db
from fastapi import APIRouter, Request, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.operation import users, admin

router = APIRouter(tags=['User'])

get_db = db.get_db


