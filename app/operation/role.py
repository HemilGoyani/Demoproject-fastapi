
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.models import Permission, Role, Modules, AccessName
from sqlalchemy.sql import func


def create_role(name, active, db):
    exist_role = db.query(Role).filter(
        Role.name == name.title(), Role.active == active)
    get_firts = exist_role.first()

    if not get_firts:
        create_role = Role(
            name=name.title(), active=active)
        db.add(create_role)
        db.commit()

        

        modules = db.query(Modules).all()
        for module in modules:
            if name.title() == "Admin":
                permission = Permission(
                    role_id= create_role.id, module_id=module.id, access_type=AccessName.READ_WRITE.value)
                db.add(permission)
                db.commit()
            else:
                permission = Permission(
                    role_id= create_role.id, module_id=module.id, access_type=AccessName.READ.value)
                db.add(permission)
                db.commit()
        return create_role
    else:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                            detail=f"role name {name} allready exist")


def get_role(db):
    exist_role = db.query(Role).all()

    if not exist_role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='role are not exist')

    return exist_role
