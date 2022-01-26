
from logging import raiseExceptions
from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from app.models import Permission, Role, Modules, AccessName,UserRole
from sqlalchemy.sql import func


def role_permission_set(role_id, module_id, access_name, db):
    permission = Permission(
        role_id=role_id, module_id=module_id, access_type=access_name)
    db.add(permission)
    db.commit()


def create_role(name, active, db):
    exist_role = db.query(Role).filter(
        Role.name == name.title(), Role.active == active).first()

    if not exist_role:
        create_role = Role(
            name=name.title(), active=active)
        db.add(create_role)
        db.commit()

        modules = db.query(Modules).all()
        for module in modules:
            if name.title() == "Admin":
                role_permission_set(create_role.id, module.id,
                                    AccessName.READ_WRITE.value, db)
            else:
                role_permission_set(create_role.id, module.id,
                                    AccessName.READ.value, db)
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

def delete_role(role_id,db):
    check_roles = db.query(Role).filter(Role.id == role_id)
    check_roles = check_roles.first()
    if not check_roles:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'role_id {role_id} is not found')
    else:
        user_role = db.query(UserRole).filter(role_id == role_id).first()
        if user_role:
            raise HTTPException(status.HTTP_207_MULTI_STATUS,detail= f"role {role_id} is reference to the user_role table, not deleted")
        check_roles.delete(synchronize_session=False)
        db.commit()
        return {"detail": f"user id {role_id} is deleted"}
    
def get_role_permission(role_id,db):
    #check role_id exist or not
    check_roles = db.query(Role).filter(Role.id == role_id).first()
    
    if not check_roles:
       raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'role_id {role_id} is not found')
    
    # get role permission
    get_role_permission = db.query(Permission).filter(Permission.role_id == role_id).all()
    return get_role_permission