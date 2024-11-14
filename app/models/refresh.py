from pydantic import BaseModel


class Refresh(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    refresh_token: str
    access_token: str