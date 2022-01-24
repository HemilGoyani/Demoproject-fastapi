from app.database import db
from fastapi import HTTPException
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Brand, Product

def create(brand, db):
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
            status_code=404, detail="allready brand is exist")

def getall(db):
    get_brand = db.query(Brand).all()
    
    if not get_brand:
        raise HTTPException(status_code=404, detail="Brand is not present")
    return get_brand