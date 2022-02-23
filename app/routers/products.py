from http.client import HTTPException
import shutil
from app.database import db
from fastapi import APIRouter, Form, Path, status, Depends, Request, UploadFile, File
from app import schemas
from sqlalchemy.orm.session import Session
from app.operation import products
from typing import List, Optional
from app.models import AccessName
from app. util import has_permission
from fastapi.responses import FileResponse

module_name = 'Product'
router = APIRouter(prefix='/product', tags=["Product"])
get_db = db.get_db


def image_save(image):
    with open('media/'+image.filename, "wb")as buffer:
        shutil.copyfileobj(image.file, buffer)


@router.get('/')
def imges(name: str):
    img = FileResponse(f"media/{name}")
    if img:
        return img
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Image not found")


@router.post('/create/{brand_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.Getproducts)
async def create_product(request: Request, brand_id: int, email: str, name: str = Form(...), active: bool = Form(...), image: Optional[UploadFile] = File(...), db: Session = Depends(get_db)):
    image_save(image)
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return await products.create_product(brand_id, name, active, image.filename, email, db)


@router.get('/all', status_code=status.HTTP_200_OK, response_model=List[schemas.Getproducts])
async def getall_product(request: Request, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [
            AccessName.READ_WRITE, AccessName.READ]))
    return products.getall_products(db)


@router.put('/update', status_code=status.HTTP_201_CREATED, response_model=schemas.Getproducts)
async def update_product(request: Request, product_id: int, brand_id: int, name: Optional[str] = Form(None), active: Optional[bool] = Form(True), image: Optional[UploadFile] = File(...), db: Session = Depends(get_db)):
    image_save(image)
    #Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return products.update_product(product_id, brand_id, name, active, image.filename, db)


@router.delete('/delete/{product_id}', status_code=status.HTTP_200_OK)
async def delete_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return products.delete_product(product_id, db)
