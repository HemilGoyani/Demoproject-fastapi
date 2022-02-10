from ast import Pass
from app.database import db
from fastapi import APIRouter, Request, status, Depends, HTTPException
from typing import List
from app.models import Usersignup,Permission
from app.operation import user_management
import jwt
from app.authentication import SECRET_KEY, SECURITY_ALGORITHM
from fastapi.responses import JSONResponse
from app.database import db


def get_user(request, db):
    token = request.headers.get('Authorization')
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[
                                SECURITY_ALGORITHM])
            user = db.query(Usersignup).filter(Usersignup.email == payload.get('email')).first()

            data = user_management.getuser_permission(user.id, db)
            return data
        except:
             return JSONResponse(content={"detail": "INVALID TOKEN"}, status_code=status.HTTP_401_UNAUTHORIZED)
    elif not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    # else:
    #     Pass
    #     #return JSONResponse(content={"detail": "Authorization header missing"}, status_code=status.HTTP_401_UNAUTHORIZED)
   