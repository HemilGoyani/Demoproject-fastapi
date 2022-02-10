import hashlib
import datetime
from app.database import db
from fastapi import HTTPException, status
from app.models import Permission, Role, Usersignup, UserRole, Email_token, Usersignup, AccessName
import uuid
import utils.email
from app.authentication import generate_token
from app.util import module_permission, get_permission, commit_data, delete_data

get_db = db.get_db

module_name = 'Usermanagement'
access_type = AccessName.READ_WRITE


def create_users(request, user, db):
    data = module_permission(request, db, module_name, access_type)
    if data:
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
            commit_data(create_user)

            # user_role table enter the data
            for role in role_id:
                user_role = UserRole(user_id=create_user.id, role_id=role)
                commit_data(user_role, db)
            return create_user
        else:
            raise HTTPException(
                status_code=status.HTTP_207_MULTI_STATUS, detail="allready email is exist")
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")


def getall_users(request, db):
    data = module_permission(request, db, module_name, access_type) or module_permission(
        request, db, module_name, access_type=AccessName.READ)
    if data:
        user = db.query(Usersignup).all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="user is not present")
        return user


def getuser_id(request, id, db):
    data = module_permission(request, db, module_name, access_type) or module_permission(
        request, db, module_name, access_type=AccessName.READ)
    if data:
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
            commit_data(add_role)

    if role_detete:
        for role in role_detete:
            user_role = db.query(UserRole).filter(
                UserRole.user_id == user_id, UserRole.role_id == role)
            user_role.delete(synchronize_session=False)
            db.commit()


def update_user(request, user_id, data, db):
    data = module_permission(request, db, module_name, access_type)
    if data:
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
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")


def remove(request, user_id, db):
    data = module_permission(request, db, module_name, access_type)
    if data:
        user = db.query(Usersignup).filter(Usersignup.id == user_id)
        users = user.first()

        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"id {user_id} is not found")
        user_roles = db.query(UserRole).filter(UserRole.user_id == user_id)
        # user_role = user_roles.all()
        delete_data(user_roles, db)

        delete_data(user, db)
        return {"detail": f"user id {user_id} is deleted"}
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")


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
    commit_data(save_token, db)

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


def change_password(id, data, db):
    getuser = db.query(Usersignup).filter(Usersignup.id == id)
    user = getuser.first()

    hash_password_old = hashlib.md5(data.oldpassword.encode())
    hash_password_new = hashlib.md5(data.newpassword.encode())

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if user.password == hash_password_old.hexdigest():
        if data.newpassword == data.confirm_new_password:
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
    delete_data(disable_token, db)
    return user


def getuser_permission(user_id, db):
    return get_permission(user_id, db)


def update_user_role_permission(request, user_id, role_id, data, db):
    data = module_permission(request, db, module_name, access_type)
    if data:
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
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="not permission to the READ_WRITE")
