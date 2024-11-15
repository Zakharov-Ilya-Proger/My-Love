import psycopg2
from fastapi import HTTPException

from config import connector
from models import Login, LoggedIn, Reset
from settings import settings
from tokens import create_access_token


async def check_user(user: Login):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        if user.mail != '':
            cur.execute('''SELECT users.id, users.name, secondname, roles.name, code, mail, groups.group_code 
                                    FROM users
                                    JOIN roles ON roles.id = users.role_id
                                    JOIN groups ON groups.id = users.group_id
                                    WHERE mail = %s AND password = %s''',
                        (user.mail, user.password))
        else:
            cur.execute('''SELECT users.id, users.name, secondname, roles.name, code, mail, groups.group_code
                                    FROM users
                                    JOIN roles ON roles.id = users.role_id
                                    JOIN groups ON groups.id = users.group_id
                                    WHERE phone = %s AND password = %s''',
                        (user.phone, user.password))
        data = cur.fetchone()
        cur.close()
        conn.close()
        if data is None:
            return [], None
        else:
            return LoggedIn(data={
                    'id':data[0],
                    'name':data[1],
                    'secondname':data[2]},
                    access_token=create_access_token({
                                             'id': data[0],
                                             'role': data[3],
                                             'code': data[4],
                                             'mail': data[5],
                                             'group': data[6]},
                                              expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                    refresh_token=create_access_token({
                                             'id': data[0],
                                             'role': data[3],
                                             'code': data[4],
                                             'name': data[1],
                                             'secondname': data[2],
                                             'mail': data[5],
                                             'group': data[6]
                                            }, expires_delta=settings.REFRESH_TOKEN_EXPIRED_HOURS)), True
    except (Exception, psycopg2.DataError) as e:
        raise HTTPException(status_code=500, detail=f'DB Error: {e}')


async def set_time_code(mail, random_code):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE users SET reset_code = %s WHERE mail = %s''',
                    (random_code, mail))
        cur.close()
        conn.commit()
        conn.close()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail='User not found')
        else:
            return True
    except (Exception, psycopg2.DataError) as e:
        raise HTTPException(status_code=500, detail=f'DB Error: {e}')


async def reset_password(request: Reset):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE users SET password = %s WHERE mail = %s AND reset_code = %s''',
                    (request.password, request.mail, request.reset_code))
        cur.close()
        conn.commit()
        conn.close()
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail='User not found or code is incorrect')
        else:
            return True
    except (Exception, psycopg2.DataError) as e:
        raise HTTPException(status_code=500, detail=f'DB Error: {e}')
