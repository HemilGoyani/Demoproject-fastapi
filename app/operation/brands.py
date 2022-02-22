from fastapi import HTTPException, status
from app.models import Brand, Product
from app.util import commit_data, delete_data, get_data,check_data


def create_brand(brand, db):
    existbrand = check_data(Brand,brand.name,db)

    if existbrand:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Brand {brand.name} is allready exist")

    create_brand = Brand(name=brand.name, active=brand.active)
    commit_data(create_brand, db)
    return create_brand


def getall_brand(db):

    get_brand = db.query(Brand).all()
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

    exist_name = check_data(Brand,brand.name,db)
    if exist_name:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                            detail=f"Brand {brand.name} allready exist")
    if brand.name:
        get_first.name = brand.name

    if brand.active is not None:
        get_first.active = brand.active
    db.add(get_first)
    db.commit()
    db.refresh(get_first)
    return get_first


def delete_brand(id, db):
    brand = get_data(Brand, id, db)
    get_firts = brand.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} not found")
    exist_brand = db.query(Product).filter(Product.brand_id == id).first()
    if not exist_brand:
        delete_data(brand, db)
        return {"detail": f"Brand id {id} is deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {id} not delete, brand allocated with product")
