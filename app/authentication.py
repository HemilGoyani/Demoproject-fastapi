from operator import lt
import jwt
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Union, Any
from pydantic import BaseModel
from fastapi import Depends, HTTPException, Request, status
import os
from fastapi.security import HTTPBearer
from pydantic import ValidationError

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = 'string@123'


def generate_token(email: Union[str, Any]):
    expire = datetime.utcnow() + timedelta(
        minutes= 60
    )
    to_encode = {
        "exp": expire, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,
                             algorithm=SECURITY_ALGORITHM)
    
    return {"token": encoded_jwt}


# def token_valid(request):

#     token = request.headers.get('Authorization')
#     print
#     if not token:
#         return JSONResponse(content={"detail":"Authorization header missing"},status_code=status.HTTP_401_UNAUTHORIZED)
#     try:
#         payload = jwt.decode(token, SECRET_KEY,
#                              algorithm=SECURITY_ALGORITHM)
#         email= payload.get("email")
#         print("check : ",email)
        
#         if not email:
            
#             return JSONResponse(content={"detail":"Invalid token"},status_code=status.HTTP_403_FORBIDDEN)

#         if payload.get('exp') < datetime.now():
#             return JSONResponse(content={"detail":"Token expired"},status_code=status.HTTP_403_FORBIDDEN)
#         return email    
#     except:
#         return JSONResponse(content={"detail":"invalid token"},status_code=status.HTTP_401_UNAUTHORIZED)