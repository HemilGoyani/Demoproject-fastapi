from ast import Pass
from app.database import db
from fastapi import HTTPException, status
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Brand, Product


def create_brand(brand, db):
    existbrand = db.query(Brand).filter(
        Brand.name == brand.name, Brand.active == brand.active)
    getfirst = existbrand.first()

    if not getfirst:
        create_brand = Brand(name=brand.name, active=brand.active)
        db.add(create_brand)
        db.commit()
        return create_brand

    else:
        raise HTTPException(
            status_code=status.HTTP_207_MULTI_STATUS, detail="allready brand is exist")


def getall_brand(db):
    get_brand = db.query(Brand).all()

    if not get_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand is not present")
    return get_brand

def getaid_brand(brand_id,db):
    get_brand = db.query(Brand).filter(Brand.id == brand_id).first()
    
    if not get_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand id {brand_id} not present")
    return get_brand

def update_brand(id, brand, db):
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


def delete_brand(id, db):
    brand = db.query(Brand).filter(Brand.id == id)
    get_firts = brand.first()
    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} is not found")
    exist_brand= db.query(Product).filter(Product.brand_id == id).first()
    if not exist_brand:
        brand.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"Brand id {id} is deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} is not delete, reason product is available")