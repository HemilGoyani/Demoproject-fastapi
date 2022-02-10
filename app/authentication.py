import jwt
from datetime import datetime, timedelta
from typing import Union, Any

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = 'string@123'


def generate_token(email: Union[str, Any]):
    expire = datetime.utcnow() + timedelta(
        minutes= 60
    )
    to_encode = {
        "exp": expire, "email": email
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,
                             algorithm=SECURITY_ALGORITHM)
    
    return {"token": encoded_jwt}
