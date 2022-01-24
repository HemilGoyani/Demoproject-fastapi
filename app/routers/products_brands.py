from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import products_brands

router = APIRouter()

get_db = db.get_db

@router.post('/brands/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getbrands,tags=["Brand"])
async def create(brand: schemas.Reubrands, db: Session = Depends(get_db)):
    return products_brands.create(brand, db)


@router.get('/brands/all', response_model=schemas.Getbrands, tags=['Brand'])
async def getall(db: Session = Depends(get_db)):
    return products_brands.getall(db)