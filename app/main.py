from fastapi import FastAPI
from app.routers import products, brands, admin, users

app = FastAPI()

@app.get("/")
def root():
    return "Demo-Project"

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(brands.router)
app.include_router(products.router)


