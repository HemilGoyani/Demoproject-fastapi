from ast import Pass
from app.database import db
from fastapi import HTTPException, status
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Brand, Product


def create_product(id, product, db):
    get_productid = db.query(Brand).filter(Brand.id == id).first()
    if get_productid:
        exist_product = db.query(Product).filter(
            Product.brand_id == id, Product.name == product.name)
        get_firts = exist_product.first()
        if not get_firts:
            create_product = Product(
                brand_id=id, name=product.name, active=product.active)
            db.add(create_product)
            db.commit()
            return create_product
        else:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                                detail=f"Product is available for the brand_id {id}")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"brand_id {id} not available")


def getall_products(db):
    get_product = db.query(Product).all()

    if not get_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Products not available")
    return get_product


def update_product(id, brand_id, product, db):
    get_product = db.query(Product).filter(Product.id == id)
    get_firts = get_product.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {id} is not available")
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} is not available")
    get_product.update({"brand_id": brand_id,
                       "name": product.name, "active": product.active})
    db.commit()
    return get_firts


def delete_product(product_id, db):
    get_product = db.query(Product).filter(Product.id == product_id)
    get_firts = get_product.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {product_id} is not found")
    get_product.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"Product id {product_id} is deleted"}
