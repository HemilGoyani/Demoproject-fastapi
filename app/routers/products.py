from app.database import db
from fastapi import APIRouter, status, Depends, Request,UploadFile,File
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import products
from typing import List
from app.models import AccessName
from app. util import has_permission

module_name = 'Product'

router = APIRouter(prefix='/product',tags=["Product"])
get_db = db.get_db


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getproducts)
async def create_product(request: Request, brand_id: int, product: schemas.Reuproducts, image: UploadFile = File(...) , db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return products.create_product(brand_id, product,image, db)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.Getproducts])
async def getall_product(request: Request, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE,AccessName.READ]))
    return products.getall_products(db)


@router.put('/update/{product_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.Getproducts)
async def update_product(request: Request, product_id: int, brand_id: int, product: schemas.Reuproducts, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return products.update_product(product_id, brand_id, product, db)


@router.delete('/delete/{product_id}', status_code=status.HTTP_200_OK)
async def delete_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return products.delete_product(product_id, db)
