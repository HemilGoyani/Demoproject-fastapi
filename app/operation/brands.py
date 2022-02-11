from fastapi import HTTPException, status
from app.models import Brand, Product, AccessName
from app.util import module_permission, commit_data, delete_data, get_data


def create_brand(brand, db):
    existbrand = db.query(Brand).filter(
        Brand.name == brand.name, Brand.active == brand.active).first()

    if not existbrand:
        create_brand = Brand(name=brand.name, active=brand.active)
        commit_data(create_brand, db)
        return create_brand

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="allready brand is exist")


def getall_brand(db):

    get_brand = db.query(Brand).all()

    if not get_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand is not present")
    return get_brand


def getid_brand(brand_id, db):

    get_brand = get_data(Brand, brand_id, db).first()

    if not get_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand id {brand_id} not present")
    return get_brand


def update_brand(id, brand, db):

    get_brand = get_data(Brand, id, db)
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

    brand = get_data(Brand, id, db)
    get_firts = brand.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} is not found")
    exist_brand = db.query(Product).filter(Product.brand_id == id).first()
    if not exist_brand:
        delete_data(brand, db)
        return {"detail": f"Brand id {id} is deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} is not delete, reason product is available")
