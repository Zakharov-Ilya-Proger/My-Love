from pydantic import BaseModel


class Reset(BaseModel):
    new_password: str
    reset_code: int