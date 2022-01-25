import binascii
import hashlib

from mysqlx import Session
from app.database import db
from fastapi import HTTPException, status
from typing import List
from app.models import Role, Usersignup, UserRole,Permission,Modules,AccessName
from sqlalchemy.sql import func
get_db = db.get_db


def create_users(user, db):
    #password convert to hashpassword
    hash_password = hashlib.md5(user.password.encode())

    # check the user are exist or not
    existuser = db.query(Usersignup).filter(
        Usersignup.email == user.email, Usersignup.password == hash_password.hexdigest())
    getfirst = existuser.first()

    if not getfirst:
        #create user
        create_user = Usersignup(name=user.name, address=user.address,
                                 email=user.email, password=hash_password.hexdigest(), isAdmin=user.isAdmin)
        db.add(create_user)
        db.commit()

        qry = db.query(func.max(Usersignup.id).label("max_id"),)
        res = qry.one()
        max_id = res.max_id

        # get all modules
        modules = db.query(Modules).all()

        #add user_role table
        if user.isAdmin == True:
            admin = db.query(Role).filter(Role.name == "Admin").first()
            user_role = UserRole(user_id=max_id, role_id=admin.id)
            
        else:
            user = db.query(Role).filter(Role.name == "User").first()
            user_role = UserRole(user_id=max_id, role_id=user.id)
            
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

    getuser.update({"name": data.name, "address": data.address})
    db.commit()
    return user


def remove(user_id, db):

    user = db.query(Usersignup).filter(Usersignup.id == user_id)
    users = user.first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {user_id} is not found")
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"user id {user_id} is deleted"}


def assign_role(user_id, role_name, db):

    user = db.query(Usersignup).filter(Usersignup.id == user_id)
    users = user.first()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user {user_id} is not found")

    check_role = db.query(Role).filter(
        Role.name == role_name.title()).first()

    if check_role:
        assign_role = UserRole(
            user_id=user_id, role_id=check_role.id)
        db.add(assign_role)
        db.commit()
        return assign_role
    else:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                            detail=f"role name {role_name} is not exist")
