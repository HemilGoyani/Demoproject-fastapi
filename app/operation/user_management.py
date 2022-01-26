import hashlib
import datetime
from app.database import db
from fastapi import HTTPException, status
from app.models import Role, Usersignup, UserRole, Email_token, Usersignup
from sqlalchemy.sql import func
import uuid
import utils.email
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


def update_user(user_id, data, db):

    getuser = db.query(Usersignup).filter(Usersignup.id == user_id)
    user = getuser.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    role_id = data.role_id.split(",")
    for role in role_id:
        check_role_id = db.query(Role).filter(Role.id == role).first()
        if not check_role_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"role id {role} is not exist")

    delete_roles = db.query(UserRole).filter(UserRole.user_id == user_id)
    delete_roles.delete(synchronize_session=False)
    db.commit()
    for role in role_id:
        user_role = UserRole(user_id=user_id, role_id=role)
        db.add(user_role)
        db.commit()
    getuser.update(
        {"name": data.name, "address": data.address, "role_id": data.role_id})
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


def login(email, password, db):
    hash_password = hashlib.md5(password.encode())
    user = db.query(Usersignup).filter(Usersignup.email ==
                                       email, Usersignup.password == hash_password.hexdigest()).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="email and password not found")
    return user


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
    <html>
        <body>
            <div>
                <h1>passsword reset token:{0}</h1>               
            </div>
        </body>
    </html>
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
    # get_email = disable_token.first()
    # if not get_email:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    disable_token.update({"status": False})
    db.commit()
    return user
