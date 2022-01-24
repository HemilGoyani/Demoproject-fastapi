from ast import Pass
from app.database import db
from fastapi import HTTPException, status
from app import schemas
from sqlalchemy.orm.session import Session
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
        return create_module

    else:
        raise HTTPException(
            status_code=status.HTTP_207_MULTI_STATUS, detail=f"allready module {module_name} is exist")
