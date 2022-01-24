from http.client import HTTPException
from typing import Dict, List, Optional
from pydantic import BaseModel, validator
from fastapi import HTTPException, status
import re



def should_not_contains_special_char(string):
    special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if special_char.search(string):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Name should not contain special characters and number')
    return string

def validate_emails(cls, email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if email:
        for email in email.split(','):
            if not re.fullmatch(regex, email.strip()):
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="envalid email")
        return email
    return email


class Reqsignup(BaseModel):
    name: str
    address: str
    email: str
    password:str
    confirm_password: str

    contains_special_char = validator("name", allow_reuse=True)(
        should_not_contains_special_char)

    validate_email = validator(
        'email', allow_reuse=True)(validate_emails)

    @validator('confirm_password')
    def passwords_match(cls, confirm_password, values, **kwargs):
        if 'password' in values and confirm_password != values['password']:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="confirm password not match to the password field")
        return confirm_password

    
    class Config():
        orm_mode = True

class Getsignup(BaseModel):
    id: int
    name: Optional[str]
    address: Optional[str]
    email: Optional[str]
    password:Optional[str]

    class Config():
        orm_mode = True

class Update_user(BaseModel):
    name: Optional[str]
    address: Optional[str]

    contains_special_char = validator("name", allow_reuse=True)(
        should_not_contains_special_char)
    class Config():
        orm_mode = True

class login(BaseModel):
    email: str
    password: str


class Reubrands(BaseModel):
    name: str
    active: bool

    class Config():
        orm_mode = True

class Getbrands(BaseModel):
    id: Optional[int]
    name: Optional[str]
    active: Optional[bool]

    class Config():
        orm_mode = True


    
