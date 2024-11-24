from datetime import timedelta
from random import randint
from typing import Annotated
from fastapi import APIRouter, Header
from app.db.models import LoggedIn, Login, RefreshResponse, ResetInit, Reset
from app.db.user_db import check_user, set_time_code, reset_password
from app.send_code import send_email
from app.tokens import decode_token, create_access_token

user_router = APIRouter()


@user_router.post('/login', response_model=LoggedIn)
async def login(request: Login):
    response = await check_user(request)
    if isinstance(response, LoggedIn):
        return response
    raise response


@user_router.get('/refresh', response_model=RefreshResponse, description='Refresh token')
async def refresh(authorization: Annotated[str | None, Header()] = None):
    decoded_token = decode_token(authorization)
    decoded_token.pop('exp')
    response = RefreshResponse(
        access_token=create_access_token(
            expires_delta=timedelta(minutes=15),
            data={
                'id': decoded_token['id'],
                'role': decoded_token['role'],
                'code': decoded_token['code'],
                'mail': decoded_token['mail'],
                'group': decoded_token['group']
            }),
        refresh_token=create_access_token(
            expires_delta=timedelta(days=1),
            data=decoded_token),
    )
    return response


@user_router.post('/reset')
async def reset(password: ResetInit):
    code = randint(1000, 9999)
    response = await set_time_code(password.mail, code)
    send_email(to_email=password.mail, subject='Password Reset Code', body=f'Code: {code}')
    raise response


@user_router.put('/reset/confirm')
async def reset_confirm(request: Reset):
    response = await reset_password(request)
    raise response
