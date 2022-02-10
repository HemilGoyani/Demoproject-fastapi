from fastapi import HTTPException, status
from app.models import Brand, Product, AccessName
from app.util import module_permission, commit_data, delete_data, get_data

module_name = 'Brand'
access_type = AccessName.READ_WRITE


def create_brand(request, brand, db):

    data = module_permission(request, db, module_name, access_type)
    if data:
        existbrand = db.query(Brand).filter(
            Brand.name == brand.name, Brand.active == brand.active).first()

        if not existbrand:
            create_brand = Brand(name=brand.name, active=brand.active)
            commit_data(create_brand, db)
            return create_brand

        else:
            raise HTTPException(
                status_code=status.HTTP_207_MULTI_STATUS, detail="allready brand is exist")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")


def getall_brand(request, db):
    data = module_permission(request, db, module_name, access_type) or module_permission(
        request, db, module_name, access_type=AccessName.READ)
    if data:
        get_brand = db.query(Brand).all()

        if not get_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Brand is not present")
        return get_brand


def getid_brand(request, brand_id, db):
    data = module_permission(request, db, module_name, access_type) or module_permission(
        request, db, module_name, access_type=AccessName.READ)
    if data:
        get_brand = db.query(Brand).filter(Brand.id == brand_id).first()

        if not get_brand:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Brand id {brand_id} not present")
        return get_brand


def update_brand(request, id, brand, db):
    data = module_permission(request, db, module_name, access_type)
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
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")


def delete_brand(request, id, db):
    data = module_permission(request, db, module_name, access_type)
    if data:
        brand = db.query(Brand).filter(Brand.id == id)
        get_firts = brand.first()
        # get_firts = get_data(Brand,id,db)
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
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")
