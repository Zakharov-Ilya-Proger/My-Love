import datetime
from random import randint
from typing import Annotated
from fastapi import APIRouter, HTTPException, Header

from app.db.admin_db import check_admin, set_time_code_admin, reset_password_admin
from app.db.models import LoggedIn, Login, ResetInit, Reset, RefreshResponse
from app.tokens import create_access_token, decode_token
from app.send_code import send_email

admin_router = APIRouter()


@admin_router.post('/login', response_model=LoggedIn)
async def login(request: Login):
    response, status = await check_admin(request)
    if status is None:
        raise HTTPException(status_code=404, detail='No such user')
    elif status is False:
        raise HTTPException(status_code=500, detail=f'DB error {response}')
    else:
        return response


@admin_router.get('/refresh', response_model=RefreshResponse, description='Refresh token')
async def refresh(authorization: Annotated[str | None, Header()] = None):
    decoded_token = decode_token(authorization)
    decoded_token.pop('exp')
    response = RefreshResponse(
        access_token=create_access_token(
            expires_delta=datetime.timedelta(minutes=15),
            data={
                'id': decoded_token['id'],
                'role': decoded_token['role'],
                'code': decoded_token['code'],
                'mail': decoded_token['mail']
            }),
        refresh_token=create_access_token(
            expires_delta=datetime.timedelta(days=1),
            data=decoded_token),
    )
    return response


@admin_router.post('/reset')
async def reset(password: ResetInit):
    code = randint(1000, 9999)
    await set_time_code_admin(password.mail, code)
    send_email(to_email=password.mail, subject='Password Reset Code', body=f'Code: {code}')
    raise HTTPException(status_code=200, detail='Time code is ready')


@admin_router.put('/reset/confirm')
async def reset_confirm(request: Reset):
    await reset_password_admin(request)
    raise HTTPException(status_code=200, detail='A new password has been set')
