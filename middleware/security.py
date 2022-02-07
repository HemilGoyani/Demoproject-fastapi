from fastapi import FastAPI, Request
import time
from fastapi.security import HTTPBearer
from app.authentication import validate_token
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, Response


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

async def check_token_valid(request:Request, call_next):
    token = validate_token()
    response = await call_next(request)
    response.headers["token_message"] = str(token)
    return response

async def TestCustomMiddleware(request: Request, call_next):
     print("Middleware works!")
     response = await call_next(request)
     return response

# async def verify_token(request: Request, call_next):
#     if request.headers['token']:
#         check_email_credential = validate_token(request.headers['token'])
#         response = await call_next(request)
#         return response
#     else:
#         return JSONResponse(content={
#             "message": "we do not allow token"
#         }, status_code=401)