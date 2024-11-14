import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from settings import settings

def create_access_token(data: dict, expires_delta: timedelta):
    copy_data = data.copy()
    time_now = datetime.now()
    minutes_after_23 = (time_now.hour - 23) * 60 + time_now.minute
    if expires_delta == timedelta(hours=1):
        if minutes_after_23 >= 0:
            expire = datetime.combine(datetime.today() + timedelta(days=1), datetime.min.time()) + timedelta(minutes=minutes_after_23)
        else:
            expire = time_now + expires_delta
    elif expires_delta == timedelta(minutes=15):
        if minutes_after_23 >= 45:
            expire = (datetime.combine(datetime.today() + timedelta(days=1), datetime.min.time()) +
                      timedelta(minute=time_now.minute % 45))
        else:
            expire = time_now + expires_delta
    else:
        expire = time_now + expires_delta

    copy_data.update({"exp": expire})
    return jwt.encode(copy_data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str = Depends(OAuth2PasswordBearer)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
