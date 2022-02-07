from operator import lt
import jwt 
from datetime import datetime, timedelta
from typing import Union, Any
from pydantic import BaseModel
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = 'string@123'

def generate_token(email: Union[str, Any]):
    expire = datetime.utcnow() + timedelta(
        days=3 
    )
    to_encode = {
        "exp": expire, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=SECURITY_ALGORITHM)
    return encoded_jwt

 
def validate_token():

    try:
        payload = jwt.decode(SECRET_KEY, algorithms=[SECURITY_ALGORITHM])

        if payload.get('exp') < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('email')
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )