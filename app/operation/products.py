from fastapi import HTTPException, status
from app.models import Brand, Product
from app. util import commit_data, delete_data, get_data
from fastapi_mail import FastMail, MessageSchema
from utils.email import email_send


async def create_product(id, name, active, image, email, db):
    get_brand = get_data(Brand, id, db).first()
    if get_brand:
        exist_product = db.query(Product).filter(
            Product.brand_id == id, Product.name == name).first()

        if exist_product:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                                detail=f"Product is available for the brand_id {id}")

        create_product = Product(
            brand_id=id, name=name, active=active, product_image=image)

        context = {
            "name": name,
            "image": image,
            "message": "Product created"
        }

        message = MessageSchema(
            subject="Our product created",
            recipients=[email],
            body=context
        )

        fm = FastMail(email_send)
        await fm.send_message(message, template_name="product.html")

        commit_data(create_product, db)
        return create_product

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Brand_id {id} not available")


def getall_products(db):

    get_product = db.query(Product).all()
    return get_product


def update_product(product_id, brand_id, name, active, image, db):
    get_product = get_data(Product, product_id, db).first()
    
    if not get_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {product_id} is not available")

    brand = get_data(Brand, brand_id, db).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Brand id {brand_id} is not available")
    if name:
        get_product.name = name
    if active is not None:
        get_product.active = active
    if image:
        get_product.product_image = image 
    commit_data(get_product, db)
    return get_product


def delete_product(product_id, db):
    get_product = get_data(Product, product_id, db)
    get_firts = get_product.first()

    if not get_firts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {product_id} is not found")
    delete_data(get_product)
    return {"detail": f"Product id {product_id} is deleted"}
