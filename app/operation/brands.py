from ast import Pass

from sqlalchemy import true
from app.database import db
from fastapi import HTTPException, status
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Brand, Product, Usersignup, AccessName
from app.operation import users
module_name = 'Brand'
access_type = AccessName.READ_WRITE

#common fuction permission access or not 
def module_permission(request,db,module_name,access_type):
    data = users.get_user(request,db)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Authorization header missing")
    for i in data:
        if i.get('module_name') == module_name:
            if i.get('access_type') == access_type:
                return True
            return False

def create_brand(request, brand, db):
    
    data = module_permission(request,db,module_name,access_type)
    
    if data:
        existbrand = db.query(Brand).filter(
        Brand.name == brand.name, Brand.active == brand.active).first()

        if not existbrand:
            create_brand = Brand(name=brand.name, active=brand.active)
            db.add(create_brand)
            db.commit()
            return create_brand

        else:
            raise HTTPException(
                status_code=status.HTTP_207_MULTI_STATUS, detail="allready brand is exist")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not permission to the READ_WRITE")

    

def getall_brand(request,db):
    data = module_permission(request,db,module_name,access_type) or module_permission(request,db,module_name,access_type= AccessName.READ)
    if data:
        get_brand = db.query(Brand).all()

        if not get_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Brand is not present")
        return get_brand
            

def getid_brand(request,brand_id, db):
    data = module_permission(request,db,module_name,access_type) or module_permission(request,db,module_name,access_type= AccessName.READ)
    if data:
        get_brand = db.query(Brand).filter(Brand.id == brand_id).first()

        if not get_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand id {brand_id} not present")
        return get_brand


def update_brand(request, id, brand, db):
    data = module_permission(request,db,module_name,access_type)
    if data:
        get_brand = db.query(Brand).filter(Brand.id == id)
        get_first = get_brand.first()

        if not get_first:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"brand_id {id} not found")

        exist_name = db.query(Brand).filter(Brand.name == brand.name).first()
        if not exist_name:
            get_brand.update({"name": brand.name, "active": brand.active})
            db.commit()
            return get_first
        else:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                                detail=f"Brand_name {brand.name} allready exist")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not permission to the READ_WRITE")

def delete_brand(request,id, db):
    data = module_permission(request,db,module_name,access_type)
    if data:
        brand = db.query(Brand).filter(Brand.id == id)
        get_firts = brand.first()
        if not get_firts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Brand id {id} is not found")
        exist_brand = db.query(Product).filter(Product.brand_id == id).first()
        if not exist_brand:
            brand.delete(synchronize_session=False)
            db.commit()
            return {"detail": f"Brand id {id} is deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Brand id {id} is not delete, reason product is available")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not permission to the READ_WRITE")