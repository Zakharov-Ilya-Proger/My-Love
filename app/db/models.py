from pydantic import BaseModel

class Login(BaseModel):
    phone: str = None
    mail: str = None
    password: str


class LoggedIn(BaseModel):
    data: dict
    access_token: str
    refresh_token: str


class Refresh(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    refresh_token: str
    access_token: str


class ResetInit(BaseModel):
    mail: str


class Reset(BaseModel):
    mail: str
    new_password: str
    reset_code: int