from fastapi import HTTPException, status
from fastapi import status, Depends, HTTPException
from app.models import Usersignup,Modules,Permission,AccessName
from app import models
import jwt
from app.authentication import SECRET_KEY, SECURITY_ALGORITHM
from fastapi.responses import JSONResponse

# common fuction permission access or not
def module_permission(request, db, module_name, access_type):
    token = request.headers.get('Authorization')
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[
                SECURITY_ALGORITHM])
            user = db.query(Usersignup).filter(
                Usersignup.email == payload.get('email')).first()

            data = get_permission(user.id, db)
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Authorization header missing")
            for i in data:
                if i.get('module_name') == module_name:
                    if i.get('access_type') == access_type:
                        return True
                    return False
        except:
            return JSONResponse(content={"detail": "INVALID TOKEN"}, status_code=status.HTTP_401_UNAUTHORIZED)
    elif not token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="Authorization header missing")


def get_permission(user_id,db):
    get_user = db.query(Usersignup).filter(Usersignup.id == user_id).first()

    if not get_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"user id {user_id} not found")
    role_id = get_user.role_id.split(",")
    record = []

    module_list = db.query(Modules).all()

    for module in module_list:
        get_permission = db.query(Permission).filter(
            Permission.role_id.in_(role_id), Permission.module_id == module.id).all()
        dic = {
            "module_name": module.name,
            "access_type": models.AccessName.NONE
        }
        for data in get_permission:
            if data.access_type.value == AccessName.READ_WRITE.value:
                dic.update({
                    "access_type": data.access_type
                })
                break
            elif data.access_type.value == AccessName.READ.value:
                dic.update({
                    "access_type": data.access_type
                })
        record.append(dic)
    return record


def commit_data(table,db):
    db.add(table)
    db.commit()

def delete_data(table,db):
    table.delete(synchronize_session=False)
    db.commit()  
