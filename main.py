from datetime import timedelta
from random import randint
from typing import Annotated

import uvicorn
from fastapi import FastAPI, HTTPException, Header
from db import check_user, set_time_code, reset_password
from models import LoggedIn, Login, RefreshResponse, ResetInit, Reset
from send_code import send_email
from settings import settings
from tokens import decode_token, create_access_token

app = FastAPI()

@app.get("/")
async def root():
    return {'message': 'Hello World'}

@app.post('/login', response_model=LoggedIn)
async def login(request: Login):
    response, status = await check_user(request)
    if status is None:
        raise HTTPException(status_code=404, detail='No such user')
    elif status is False:
        raise HTTPException(status_code=500, detail=f'DB error {response}')
    else:
        return response

@app.get('/refresh', response_model=RefreshResponse)
async def refresh(refresh_token: Annotated[str | None, Header()] = None):
    decoded_token = decode_token(refresh_token)
    decoded_token.pop('exp')
    response = RefreshResponse(
        access_token=create_access_token(
            expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            data={
                'id':decoded_token['id'],
                'role':decoded_token['role'],
                'code':decoded_token['code'],
                'mail':decoded_token['mail'],
                'group':decoded_token['group']
            }),
        refresh_token=create_access_token(
            expires_delta=timedelta(settings.REFRESH_TOKEN_EXPIRED_HOURS),
            data=decoded_token),
    )
    return response

@app.post('/reset')
async def reset(password: ResetInit):
    code = randint(1000, 9999)
    await set_time_code(password.mail, code)
    send_email(to_email=password.mail, subject='Password Reset Code', body=f'Your verification code is: {code}')
    raise HTTPException(status_code=200, detail='Time code is ready')

@app.post('/reset/confirm')
async def reset_confirm(request: Reset):
    await reset_password(request)
    raise HTTPException(status_code=200, detail='A new password has been set')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=settings.APP_PORT)
