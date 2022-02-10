from urllib.request import Request
from fastapi import FastAPI
from app.authentication import SECRET_KEY
from middleware.security import check_token_valid
from app.routers import products, brands, modules, user_management, role
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.middleware('http')(check_token_valid)


@app.get("/")
def root():
    return "Demo-Project"


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_management.router)
app.include_router(modules.router)
app.include_router(role.router)
app.include_router(brands.router)
app.include_router(products.router)

