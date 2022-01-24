import binascii
import hashlib
from app.database import db
from fastapi import HTTPException, status
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.models import Usersignup
import os
get_db = db.get_db


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(5)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 5)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def create(user,value, db):
    existuser = db.query(Usersignup).filter(
        Usersignup.email == user.email, Usersignup.password == user.password)
    getfirst = existuser.first()

    if not getfirst:
        create_user = Usersignup(name=user.name, address=user.email,
                                 email=user.email, password=user.password)
        db.add(create_user)
        db.commit()
        return create_user

    else:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS, detail="allready email is exist")


def login(email, password, db):
    user = db.query(Usersignup).filter(Usersignup.email ==
                                       email, Usersignup.password == password).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email and password not found")
    return user.__dict__


def forgotpass(id, email, db):
    user = db.query(Usersignup).filter(
        Usersignup.id == id, Usersignup.email == email)
    userobj = user.first()
    if not userobj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="email and id not found")

    getpass = userobj.password
    return {"your password is": getpass}


def changepass(id, oldpassword, newpassword, confirm_new_password, db):
    getuser = db.query(Usersignup).filter(Usersignup.id == id)
    user = getuser.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if user.password == oldpassword:
        if newpassword == confirm_new_password:
            getuser.update({"password": confirm_new_password})
            db.commit()
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="newpassword and confirm_new_password is not matched")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="oldpassword is not valid")






