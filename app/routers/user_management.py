from app.database import db
from fastapi import APIRouter, status, Depends, HTTPException, Request
from app import schemas
from sqlalchemy.orm.session import Session
from typing import List
from app.operation import user_management
from app.util import has_permission
from app.models import AccessName

get_db = db.get_db

module_name = 'Usermanagement'
router = APIRouter(prefix='/user_management', tags=['User Management'])


@router.post('/create_user', status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup)
async def create_users(request: Request, user: schemas.Reqsignup, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return user_management.create_users(user, db)


@router.get('/getall_users', response_model=List[schemas.Getsignup])
async def getall_users(request: Request, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [
            AccessName.READ_WRITE, AccessName.READ]))
    return user_management.getall_users(db)


@router.get('/{user_id}', response_model=schemas.Getsignup)
async def getuserbyid(request: Request, user_id: int, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [
            AccessName.READ_WRITE, AccessName.READ]))
    return user_management.getuser_id(user_id, db)


@router.put('/{user_id}', response_model=schemas.Getsignup)
async def update_user(request: Request, user_id: int, data: schemas.Update_user, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return user_management.update_user(user_id, data, db)


@router.delete('/user_delete/{user_id}')
async def remove(request: Request, user_id: int, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return user_management.remove(user_id, db)


@router.post('/signin', response_model=schemas.Getlogin)
async def login(data: schemas.Reqlogin, db: Session = Depends(get_db)):
    return user_management.login(data, db)


@router.post('/sent_email')
async def forgot_paswords(user_id: int, email: str, db: Session = Depends(get_db)):
    return await user_management.forgot_paswords_email_sent(user_id, email, db)


@router.put('/reset-password', response_model=schemas.Getsignup)
async def reset_password(request: schemas.Reset_password, db: Session = Depends(get_db)):
    reset_token = user_management.check_reset_password_token(
        request.reset_password_token, db)
    if not reset_token:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="reset password token is expired,please request new one")
    if request.new_password != request.confirm_new_password:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="new password and confirm new password is not mach")
    return user_management.reset_password(reset_token.email, request.new_password, db)


@router.put('/change_password/{user_id}', status_code=status.HTTP_201_CREATED, response_model=schemas.Getsignup)
async def change_password(user_id: int, data: schemas.Changepassword, db: Session = Depends(get_db)):
    return user_management.change_password(user_id, data, db)


@router.get('/get_user_permission/{user_id}')
async def getuserbyid(user_id: int, db: Session = Depends(get_db)):
    return user_management.getuser_permission(user_id, db)


@router.put('/update_user_role_permission')
async def update_user_role_permission(request: Request, user_id: int, role_id: int, data: schemas.Change_permissionm, db: Session = Depends(get_db)):
    Depends(has_permission(request, db, module_name, [AccessName.READ_WRITE]))
    return user_management.update_user_role_permission(user_id, role_id, data, db)
