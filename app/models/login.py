from pydantic import BaseModel

class Login(BaseModel):
    phone: str = ''
    mail: str = ''
    password: str


class LoggedIn(BaseModel):
    data: dict
    access_token: str
    refresh_token: str