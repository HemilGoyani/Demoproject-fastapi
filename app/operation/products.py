from fastapi import HTTPException, status
from app.models import Brand, Product, AccessName
from app. util import commit_data, delete_data, get_data


def create_product(id, product, db):

    get_productid = get_data(Brand, id, db).first()
    if get_productid:
        exist_product = db.query(Product).filter(
            Product.brand_id == id, Product.name == product.name).first()

        if not exist_product:
            create_product = Product(
                brand_id=id, name=product.name, active=product.active)
            commit_data(create_product, db)
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

    get_product = get_data(Product, id, db)
    get_firts = get_product.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {id} is not available")

    brand = get_data(Brand, brand_id, db).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} is not available")
    get_product.update({"brand_id": brand_id,
                        "name": product.name, "active": product.active})
    db.commit()
    return get_firts


def delete_product(product_id, db):

    get_product = get_data(Product, product_id, db)
    get_firts = get_product.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {product_id} is not found")
    delete_data(get_product)
    return {"detail": f"Product id {product_id} is deleted"}
