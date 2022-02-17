from http.client import HTTPException
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, validator, EmailStr
from fastapi import HTTPException, status, UploadFile
import re
from app.models import AccessName

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def should_not_contains_special_char(string):
    if (string.isspace() or string.isdigit()) or len(string) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Name should not contain number and blank space  ')

    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:0123456789]')
    if special_char.search(string):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Name should not contain special characters and number')
    return string.strip()


def validate_emails(cls, email):
    if email:
        for email in email.split(','):
            if not re.fullmatch(regex, email.strip()):
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email is not valid")
        return email
    return email


def should_not_empty(cls, string):
    return_str = string.strip()
    if not return_str:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="Role_id should not contain string and blank")
    role_id = string.split(',')
    for i in role_id:
        if i.isalpha():
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Role_id should not contain string")
    return return_str


def should_not_contain_number(string):
    if (string.isspace() or string.isdigit()) or len(string) == 0:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Address should not contain number and blank space  ')
    return string

class Reqsignup(BaseModel):
    name: str
    address: str
    email: str
    password: str
    confirm_password: str
    role_id: str
    contains_special_char = validator("name", allow_reuse=True)(
        should_not_contains_special_char)

    validate_email = validator(
        'email', allow_reuse=True)(validate_emails)

    _role_id = validator("role_id", allow_reuse=True)(should_not_empty)
    _address = validator("address", allow_reuse=True)(
        should_not_contain_number)

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values, **kwargs):
        if 'password' in values and confirm_password != values['password']:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="confirm password not match to the password field")
        return confirm_password

    class Config():
        orm_mode = True


class Getsignup(BaseModel):
    id: int
    name: Optional[str]
    address: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role_id: Optional[str]

    class Config():
        orm_mode = True


class Update_user(BaseModel):
    name: Optional[str]
    address: Optional[str]
    role_id: Optional[str]

    contains_special_char = validator("name", allow_reuse=True)(
        should_not_contains_special_char)

    class Config():
        orm_mode = True


class login(BaseModel):
    email: str
    password: str


class Reubrands(BaseModel):
    name: Optional[str]
    active: Optional[bool]
    _name = validator(
        'name', allow_reuse=True)(should_not_contains_special_char)

    class Config():
        orm_mode = True


class Getbrands(BaseModel):
    id: Optional[int]
    name: Optional[str]
    active: Optional[bool]

    class Config():
        orm_mode = True


class Reuproducts(BaseModel):
    name: str
    active: bool

    class Config():
        orm_mode = True


class Getproducts(BaseModel):
    id: Optional[int]
    brand_id: Optional[int]
    name: Optional[str]
    active: Optional[bool]
    product_image: Optional[str]

    class Config():
        orm_mode = True


class Getmodule(BaseModel):
    id: Optional[int]
    name: Optional[str]

    class Config():
        orm_mode = True


class Getroles(BaseModel):
    id: Optional[int]
    name: Optional[str]
    active: Optional[bool]

    class Config():
        orm_mode = True


class Getuser_role(BaseModel):
    id: Optional[int]
    user_id: Optional[int]
    role_id: Optional[int]

    class Config():
        orm_mode = True


class Reset_password(BaseModel):
    reset_password_token: str
    new_password: str
    confirm_new_password: str

    class Config():
        orm_mode = True


class Getrole_permission(BaseModel):
    access_type: Optional[AccessName]
    id: Optional[int]
    module_name: Optional[str]
    role_id: Optional[int]

    class Config():
        orm_mode = True


class Change_permissionm(BaseModel):
    module_id: int
    access_type: AccessName

    class Config():
        orm_mode = True


class Getuser_permission(BaseModel):
    access_type: Optional[AccessName]
    id: Optional[int]
    module_name: Optional[str]

    class Config():
        orm_mode = True


class Reqlogin(BaseModel):
    email: str
    password: str

    validate_email = validator(
        'email', allow_reuse=True)(validate_emails)

    class Config():
        orm_mode = True


class Getlogin(BaseModel):
    token: Optional[str]

    class Config():
        orm_mode = True


class Changepassword(BaseModel):
    oldpassword: str
    newpassword: str
    confirm_new_password: str

    class Config():
        orm_mode = True

 
