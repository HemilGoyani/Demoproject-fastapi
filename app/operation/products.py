from ast import Pass
from fastapi import HTTPException, status
from app import schemas
from typing import List
from app.models import Brand, Product,AccessName
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

def create_product(request,id, product, db):
    data = module_permission(request,db,module_name,access_type)
    if data:
        get_productid = db.query(Brand).filter(Brand.id == id).first()
        if get_productid:
            exist_product = db.query(Product).filter(
                Product.brand_id == id, Product.name == product.name).first()

            if not exist_product:
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
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not permission to the READ_WRITE")

def getall_products(request,db):
    data = module_permission(request,db,module_name,access_type) or module_permission(request,db,module_name,access_type= AccessName.READ)
    if data:
        get_product = db.query(Product).all()

        if not get_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Products not available")
        return get_product


def update_product(request,id, brand_id, product, db):
    data = module_permission(request,db,module_name,access_type)
    if data:
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
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not permission to the READ_WRITE")

def delete_product(request,product_id, db):
    data = module_permission(request,db,module_name,access_type)
    if data:
        get_product = db.query(Product).filter(Product.id == product_id)
        get_firts = get_product.first()

        if not get_firts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Product id {product_id} is not found")
        get_product.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"Product id {product_id} is deleted"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="not permission to the READ_WRITE")