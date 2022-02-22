from sys import modules
from fastapi import HTTPException, status
from app.models import Permission, Role, Modules, AccessName
from app.models import Modules
from app.util import commit_data,delete_data,get_data,check_data

def permission(role_id, module_id, access_name, db):
    permission = Permission(
        role_id=role_id, module_id=module_id, access_type=access_name)
    commit_data(permission,db)


def create_module(module_name, db):
    exist_module = check_data(Modules,module_name,db)
    if exist_module:
        raise HTTPException(
            status_code=status.HTTP_207_MULTI_STATUS, detail=f"Module {module_name} is exist")

    create_module = Modules(name=module_name.title())
    commit_data(create_module,db)

    roles = db.query(Role).all()
    for role in roles:
        if role.name == "Admin":
            permission(role.id, create_module.id,
                        AccessName.READ_WRITE.value, db)
        else:
            permission(role.id, create_module.id,
                        AccessName.READ.value, db)
    return create_module      


def get_module(db):
    exist_module = db.query(Modules).all()
    return exist_module


def delete_module(module_id, db):
    module = get_data(Modules,module_id,db)
    first_module = module.first()
    if not first_module:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f" Module id {module_id} not found")
    permission_check = db.query(Permission).filter(
        Permission.module_id == module_id)
    delete_data(permission_check)
    delete_data(module,db)
    
    return f"Module {module_id} deleted"


def get_module_permission(module_id, db):
    # check module_id exist or not
    check_module = get_data(Modules,module_id,db).first()
    if not check_module:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Module_id {module_id} not found')

    # get module permission
    get_module_permission = db.query(Permission).filter(
        Permission.module_id == module_id).all()
    return get_module_permission
