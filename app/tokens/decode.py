import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from settings import settings


def decode_token(token: str = Depends(OAuth2PasswordBearer)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
