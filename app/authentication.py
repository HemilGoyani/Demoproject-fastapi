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
