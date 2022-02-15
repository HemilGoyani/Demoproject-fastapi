
from fastapi import HTTPException, status
from app.models import Permission, Role, Modules, AccessName, UserRole
from app.util import commit_data,delete_data,get_data


def role_permission_set(role_id, module_id, access_name, db):
    permission = Permission(
        role_id=role_id, module_id=module_id, access_type=access_name)
    commit_data(permission,db)


def create_role(name, active, db):
    exist_role = db.query(Role).filter(
        Role.name == name.title(), Role.active == active).first()

    if not exist_role:
        create_role = Role(
            name=name.title(), active=active)
        commit_data(create_role,db)

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


def delete_role(role_id, db):
    check_roles = get_data(Role,role_id,db)
    check_role = check_roles.first()
    if not check_role:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'role_id {role_id} is not found')
    else:
        user_role = db.query(UserRole).filter(
            UserRole.role_id == role_id).first()
        if not user_role:
            permission_roles = db.query(Permission).filter(
                Permission.role_id == role_id)
            delete_data(permission_roles,db)

            delete_data(check_roles,db)
            return {"detail": f"Role id {role_id} is deleted"}
        raise HTTPException(status.HTTP_207_MULTI_STATUS,
                            detail=f"Role assigned to the user")

def get_role_permission(role_id, db):
    # check role_id exist or not
    check_roles = db.query(Role).filter(Role.id == role_id).first()

    if not check_roles:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'role_id {role_id} is not found')

    # get role permission
    get_role_permission = db.query(Permission).filter(
        Permission.role_id == role_id).all()
    records = []
    for data in get_role_permission:
        obj = {
            "id": data.id,
            "access_type": data.access_type,
            "module_name": data.module.name,
            "role_id": data.role_id
        }
        records.append(obj)
    return records
