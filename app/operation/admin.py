import binascii
import hashlib
from app.database import db
from fastapi import HTTPException, status
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


def getallusers(db):
    user = db.query(Usersignup).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not present")
    return user


def getuserbyid(id, db):
    user = db.query(Usersignup).filter(Usersignup.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user is not present")
    return user


def update_user(id, data, db):
    getuser = db.query(Usersignup).filter(Usersignup.id == id)
    user = getuser.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")

    getuser.update({"name": data.name, "address": data.address})
    db.commit()
    return user
   

def remove(id, db):
    user = db.query(Usersignup).filter(Usersignup.id == id)
    users = user.first()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} is not found")
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"user id {id} is deleted"}



