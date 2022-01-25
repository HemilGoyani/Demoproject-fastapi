from ast import Pass
from app.database import db
from fastapi import HTTPException, status
from app.models import Permission, Role, Modules, AccessName
from sqlalchemy.sql import func
from typing import List
from app.models import Modules


def create_module(module_name, db):
    exist_module = db.query(Modules).filter(
        Modules.name == module_name.title())
    getfirst = exist_module.first()

    if not getfirst:
        create_module = Modules(name=module_name.title())
        db.add(create_module)
        db.commit()

        roles = db.query(Role).all()
        for role in roles:
            if role.name == "Admin":
                permission = Permission(
                    role_id=role.id, module_id= create_module.id, access_type=AccessName.READ_WRITE.value)
                db.add(permission)
                db.commit()
            else:
                permission = Permission(
                    role_id=role.id, module_id= create_module.id, access_type=AccessName.READ.value)
                db.add(permission)
                db.commit()    
        return create_module

    else:
        raise HTTPException(
            status_code=status.HTTP_207_MULTI_STATUS, detail=f"allready module {module_name} is exist")

def get_module(db):
    exist_module = db.query(Modules).all()
    if not exist_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"module not exist")
    return exist_module