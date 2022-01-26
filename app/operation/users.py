import binascii
import hashlib

from sqlalchemy import false
from app.database import db
from fastapi import HTTPException, status
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Email_token, Usersignup
import utils.email
import os
import datetime
import uuid
import datetime

get_db = db.get_db



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
                <h1>passsword reset token/{0:}</h1>               
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

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if user.password == oldpassword:
        if newpassword == confirm_new_password:
            getuser.update({"password": confirm_new_password})
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
    get_token = db.query(Email_token).filter(Email_token.reset_code == reset_password_token, Email_token.status == True, Email_token.expired_in >= now - datetime.timedelta(minutes = 10)).first()
    return get_token

def reset_password(email,new_password,db):
    getuser = db.query(Usersignup).filter(Usersignup.email == email)
    user = getuser.first()
    hash_password = hashlib.md5(new_password.encode())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    
    getuser.update({"password": hash_password.hexdigest()})
    db.commit()
    disable_token = db.query(Email_token).filter(Email_token.email== email)
    get_email = disable_token.first()
    if not get_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    disable_token.update({"status": False})
    db.commit()            
    return user
