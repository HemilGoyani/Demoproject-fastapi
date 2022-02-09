import hashlib
import datetime
from modulefinder import Module
from typing import List
from app import models
from app.database import db
from fastapi import HTTPException, status
from app.models import Permission, Role, Usersignup, UserRole, Email_token, Usersignup, Modules, AccessName
from sqlalchemy.sql import func
import uuid
from fastapi.encoders import jsonable_encoder
import utils.email
from app.authentication import generate_token
get_db = db.get_db


def create_users(user, db):
    # password convert to hashpassword
    hash_password = hashlib.md5(user.password.encode())

    # check the user are exist or not
    existuser = db.query(Usersignup).filter(
        Usersignup.email == user.email).first()

    if not existuser:
        # create user
        role_id = user.role_id.split(",")
        for role in role_id:
            check_role_id = db.query(Role).filter(Role.id == role).first()
            if not check_role_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"role id {role} is not exist")

        create_user = Usersignup(name=user.name, address=user.address,
                                 email=user.email, password=hash_password.hexdigest(), role_id=user.role_id)
        db.add(create_user)
        db.commit()

        # user_role enter data
        for role in role_id:
            user_role = UserRole(user_id=create_user.id, role_id=role)
            db.add(user_role)
            db.commit()
        return create_user
    else:
        raise HTTPException(
            status_code=status.HTTP_207_MULTI_STATUS, detail="allready email is exist")


def getall_users(db):

    user = db.query(Usersignup).all()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user is not present")
    return user


def getuser_id(id, db):

    user = db.query(Usersignup).filter(Usersignup.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user is not present")
    return user


def user_role(new_role_id, old_role_id, user_id, db):
    role_add = list(new_role_id.difference(old_role_id))
    role_detete = list(old_role_id.difference(new_role_id))

    if role_add:
        for role in role_add:
            add_role = UserRole(user_id=user_id, role_id=role)
            db.add(add_role)
            db.commit()

    if role_detete:
        for role in role_detete:
            user_role = db.query(UserRole).filter(
                UserRole.user_id == user_id, UserRole.role_id == role)
            user_role.delete(synchronize_session=False)
            db.commit()


def update_user(user_id, data, db):

    # check user exist or not
    getuser = db.query(Usersignup).filter(Usersignup.id == user_id)
    user = getuser.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    # role_id split and checked
    role_id = data.role_id.split(",")
    for role in role_id:
        check_role_id = db.query(Role).filter(Role.id == role).first()
        if not check_role_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"role id {role} is not exist")

    user_role(set(data.role_id.split(",")), set(
        user.role_id.split(",")), user_id, db)

    item = {"role_id": data.role_id}

    if data.name:
        item.update({"name": data.name})
    if data.address:
        item.update({"address": data.address})

    getuser.update(item)
    db.commit()
    return user


def remove(user_id, db):
    user = db.query(Usersignup).filter(Usersignup.id == user_id)
    users = user.first()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {user_id} is not found")
    user_roles = db.query(UserRole).filter(UserRole.user_id == user_id)
    # user_role = user_roles.all()
    user_roles.delete(synchronize_session=False)
    db.commit()

    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"user id {user_id} is deleted"}


def login(data, db):
    hash_password = hashlib.md5(data.password.encode())
    user = db.query(Usersignup).filter(Usersignup.email ==
                                       data.email, Usersignup.password == hash_password.hexdigest()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="email and password not found")
    return generate_token(data.email)
    


async def forgot_paswords_email_sent(user_id, email, db):
    # check user exist or not
    user = db.query(Usersignup).filter(
        Usersignup.id == user_id, Usersignup.email == email)
    userobj = user.first()
    if not userobj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="email and id not found")
    # create reset code and save to the database
    reset_code = str(uuid.uuid1())
    current_time = datetime.datetime.utcnow()
    save_token = Email_token(
        email=email, reset_code=reset_code, status=True,  expired_in=current_time)
    db.add(save_token)
    db.commit()

    # sent email
    subject = "forgot password"
    recipient = [email]
    message = """
        passsword reset token:{0}                    
    """.format(reset_code)

    await utils.email.send_email(subject, recipient, message)
    return {
        "reset_code": reset_code,
        "message": "we have send email for that reset password"
    }


def change_password(id, oldpassword, newpassword, confirm_new_password, db):
    getuser = db.query(Usersignup).filter(Usersignup.id == id)
    user = getuser.first()

    hash_password_old = hashlib.md5(oldpassword.encode())
    hash_password_new = hashlib.md5(newpassword.encode())

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if user.password == hash_password_old.hexdigest():
        if newpassword == confirm_new_password:
            getuser.update({"password": hash_password_new.hexdigest()})
            db.commit()
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="newpassword and confirm_new_password is not matched")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="oldpassword is not valid")


def check_reset_password_token(reset_password_token, db):

    now = datetime.datetime.utcnow()
    get_token = db.query(Email_token).filter(Email_token.reset_code == reset_password_token,
                                             Email_token.status == True, Email_token.expired_in >= now - datetime.timedelta(minutes=10)).first()
    return get_token


def reset_password(email, new_password, db):
    getuser = db.query(Usersignup).filter(Usersignup.email == email)
    user = getuser.first()
    hash_password = hashlib.md5(new_password.encode())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    getuser.update({"password": hash_password.hexdigest()})
    db.commit()
    disable_token = db.query(Email_token).filter(Email_token.email == email)
    disable_token.delete(synchronize_session=False)
    db.commit()
    return user


def getuser_permission(user_id, db):
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


def update_user_role_permission(user_id, role_id, data, db):
    get_user = db.query(Usersignup).filter(Usersignup.id == user_id)
    user = get_user.first()
    
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"user id {user_id} not found")
    roles = user.role_id.split(",")
    if str(role_id) in roles:
        
        check_permission = db.query(Permission).filter(
            Permission.role_id == role_id, Permission.module_id == data.module_id)
        check = check_permission.first()
        check_permission.update({"access_type": data.access_type})
        db.commit()
        return f"permission is changed"

    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail="role_id is not valid for this user")
