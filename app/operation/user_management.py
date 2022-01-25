import binascii
import hashlib
from app.database import db
from fastapi import HTTPException, status
from typing import List
from app.models import Role, Usersignup, UserRole
import os
get_db = db.get_db


def create_users(user, db):
    hash_password = hashlib.md5(user.password.encode())
    existuser = db.query(Usersignup).filter(
        Usersignup.email == user.email, Usersignup.password == hash_password.hexdigest())
    getfirst = existuser.first()

    if not getfirst:
        
        create_user = Usersignup(name=user.name, address=user.address,
                                 email=user.email, password= hash_password.hexdigest(),isAdmin = False)
        db.add(create_user)
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

    existrole = db.query(UserRole).filter(
        UserRole.user_id == user_id, UserRole.role_name == role_name.title())
    getfirst = existrole.first()

    if not getfirst:
        check_role = db.query(Role).filter(
            Role.name == role_name.title()).first()

        if check_role:
            assign_role = UserRole(
                user_id=user_id, role_name=role_name.title())
            db.add(assign_role)
            db.commit()
            return assign_role
        else:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                                detail=f"role name {role_name} is not exist")
    else:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,
                            detail=f"allready role {role_name} is assign to the {user_id} id")
