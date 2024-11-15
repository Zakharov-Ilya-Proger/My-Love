from pydantic import BaseModel


class ResetInit(BaseModel):
    mail: str


class Reset(BaseModel):
    mail: str
    new_password: str
    reset_code: int