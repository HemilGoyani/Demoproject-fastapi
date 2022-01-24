from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import permission
from typing import List

router = APIRouter(tags=["permission"])

get_db = db.get_db