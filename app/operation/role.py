
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.models import Role


def create_role(name, active, db):
    exist_role = db.query(Role).filter(Role.name == name.title(), Role.active == active)
    get_firts = exist_role.first()

    print(get_firts,"data show")
    if not get_firts:
        create_role = Role(
           name = name.title(), active=active)
        db.add(create_role)
        db.commit()
        return create_role
    else:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                            detail=f"role name {name} allready exist") 

def get_role(db):
    exist_role = db.query(Role).all()

    if not exist_role:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail='role are not exist')

    return exist_role