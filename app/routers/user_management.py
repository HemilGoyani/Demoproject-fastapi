from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import products
from typing import List

router = APIRouter(tags=["Usermanagement"])

get_db = db.get_db


@router.post('/Usermanagemt/create_user', status_code=status.HTTP_201_CREATED, response_model=schemas.Getproducts)
async def create_product(brand_id:int, product: schemas.Reuproducts, db: Session = Depends(get_db)):
    return products.create_product(brand_id,product, db)
