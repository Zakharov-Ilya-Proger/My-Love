from datetime import timedelta
from random import randint
from typing import Annotated
from fastapi import APIRouter, Header
from app.db.models import LoggedIn, Login, RefreshResponse, ResetInit, Reset
from app.db.teacher_db import check_teacher, set_time_code_teacher, reset_password_teacher
from app.send_code import send_email
from app.tokens import decode_token, create_access_token

teacher_router = APIRouter()


@teacher_router.post('/login', response_model=LoggedIn)
async def login(request: Login):
    response = await check_teacher(request)
    if isinstance(response, LoggedIn):
        return response
    raise response


@teacher_router.get('/refresh', response_model=RefreshResponse, description='Refresh token')
async def refresh(authorization: Annotated[str | None, Header()] = None):
    decoded_token = decode_token(authorization)
    decoded_token.pop('exp')
    response = RefreshResponse(
        access_token=create_access_token(
            expires_delta=timedelta(hours=1),
            data={
                'id': decoded_token['id'],
                'role': decoded_token['role'],
                'code': decoded_token['code'],
                'mail': decoded_token['mail']
            }),
        refresh_token=create_access_token(
            expires_delta=timedelta(days=1),
            data=decoded_token),
    )
    return response


@teacher_router.post('/reset')
async def reset(password: ResetInit):
    code = randint(1000, 9999)
    response = await set_time_code_teacher(password.mail, code)
    send_email(to_email=password.mail, subject='Password Reset Code', body=f'Code: {code}')
    raise response


@teacher_router.put('/reset/confirm')
async def reset_confirm(request: Reset):
     response = await reset_password_teacher(request)
     raise response
