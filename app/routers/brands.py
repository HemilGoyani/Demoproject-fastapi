from fastapi import APIRouter, status, Depends, Request, HTTPException
from app import schemas
from app.models import AccessName
from sqlalchemy.orm.session import Session
from app.operation import brands
from typing import List
from app.database import db
from app.util import module_permission,has_permission

module_name = 'Brand'

router = APIRouter(tags=["Brand"])
get_db = db.get_db


@router.post('/brands/create', status_code=status.HTTP_201_CREATED, response_model=schemas.Getbrands)
async def create_brand(request: Request, brand: schemas.Reubrands, db: Session = Depends(get_db)):
    Depends(has_permission(request,db,module_name,[AccessName.READ_WRITE]))
    return brands.create_brand(brand, db)


@router.get('/brands/all', status_code=status.HTTP_200_OK, response_model=List[schemas.Getbrands])
async def getall_brand(request: Request, db: Session = Depends(get_db)):
    Depends(has_permission(request,db,module_name,[AccessName.READ_WRITE,AccessName.READ]))
    return brands.getall_brand(db)


@router.get('/brands/get_id', status_code=status.HTTP_200_OK, response_model=schemas.Getbrands)
async def getaid_brand(request: Request, brand_id: int, db: Session = Depends(get_db)):
    Depends(has_permission(request,db,module_name,[AccessName.READ_WRITE,AccessName.READ]))
    return brands.getid_brand(brand_id, db)


@router.put('/brands/update', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Getbrands)
async def update_brand(request: Request, brand_id: int, brand: schemas.Reubrands, db: Session = Depends(get_db)):
    Depends(has_permission(request,db,module_name,[AccessName.READ_WRITE]))
    return brands.update_brand(brand_id, brand, db)


@router.delete('/brands/delete', status_code=status.HTTP_200_OK)
async def delete_brand(request: Request, brand_id: int, db: Session = Depends(get_db)):
    Depends(has_permission(request,db,module_name,[AccessName.READ_WRITE]))
    return brands.delete_brand(brand_id, db)
