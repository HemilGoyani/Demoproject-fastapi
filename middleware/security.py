from fastapi.responses import JSONResponse
import jwt
import time
import datetime
from fastapi import HTTPException, Request, status
import time
# from app.authentication import token_valid

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = 'string@123'


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def check_token_valid(request: Request, call_next):
    token = request.headers.get('Authorization')
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[
                                SECURITY_ALGORITHM])

            if payload.get('exp') < time.time():
                return JSONResponse(content={"detail": "Token expired"}, status_code=status.HTTP_403_FORBIDDEN)
        except:
             return JSONResponse(content={"detail": "INVALID TOKEN"}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        return JSONResponse(content={"detail": "Authorization header missing"}, status_code=status.HTTP_401_UNAUTHORIZED)
    return await call_next(request)
