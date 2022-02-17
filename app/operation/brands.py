from fastapi import HTTPException, status
from app.models import Brand, Product, AccessName
from app.util import module_permission, commit_data, delete_data, get_data


def create_brand(brand, db):
    existbrand = db.query(Brand).filter(
        Brand.name == brand.name).first()

    if not existbrand:
        create_brand = Brand(name=brand.name, active=brand.active)
        commit_data(create_brand, db)
        return create_brand

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Brand {brand.name} is allready exist")


def getall_brand(db):

    get_brand = db.query(Brand).all()

    if not get_brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
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
        
        if brand.name:
            get_first.name= brand.name
            
        if brand.active is not None:
            get_first.active= brand.active
        db.add(get_first)
        db.commit()
        db.refresh(get_first)
        return get_first
        
    raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                            detail=f"Brand_name {brand.name} allready exist")


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
