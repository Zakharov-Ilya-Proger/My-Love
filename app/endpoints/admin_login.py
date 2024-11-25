import datetime
from random import randint
from typing import Annotated
from fastapi import APIRouter, Header
from app.db.admin_db import check_admin, set_time_code_admin, reset_password_admin
from app.db.models import Login, ResetInit, Reset, RefreshResponse, LoggedInAdmin
from app.tokens import create_access_token, decode_token
from app.send_code import send_email

admin_router = APIRouter()


@admin_router.post('/login', response_model=LoggedInAdmin)
async def login(request: Login):
    response = await check_admin(request)
    if isinstance(response, LoggedInAdmin):
        return response
    raise response


@admin_router.get('/refresh', response_model=RefreshResponse, description='Refresh token')
async def refresh(authorization: Annotated[str | None, Header()] = None):
    decoded_token = decode_token(authorization)
    decoded_token.pop('exp')
    response = RefreshResponse(
        access_token=create_access_token(
            expires_delta=datetime.timedelta(hours=1),
            data={
                'id': decoded_token['id'],
                'role': decoded_token['role'],
                'code': decoded_token['code'],
                'mail': decoded_token['mail'],
                'level': decoded_token['level'],
            }),
        refresh_token=create_access_token(
            expires_delta=datetime.timedelta(days=1),
            data=decoded_token),
    )
    return response


@admin_router.post('/reset')
async def reset(password: ResetInit):
    code = randint(1000, 9999)
    response = await set_time_code_admin(password.mail, code)
    send_email(to_email=password.mail, subject='Password Reset Code', body=f'Code: {code}')
    raise response


@admin_router.put('/reset/confirm')
async def reset_confirm(request: Reset):
    response = await reset_password_admin(request)
    raise response
