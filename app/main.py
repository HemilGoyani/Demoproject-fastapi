from fastapi import FastAPI
from app.routers import signup, products_brands

app = FastAPI()

@app.get("/")
def root():
    return "Demo-Project"


app.include_router(signup.router)
app.include_router(products_brands.router)