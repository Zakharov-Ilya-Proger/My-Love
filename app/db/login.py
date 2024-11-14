from datetime import timedelta

import psycopg2
from app.db.config import connector
from app.models.login import Login, LoggedIn
from app.tokens.generate import create_access_token
from settings import settings


async def check_user(user: Login):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        if user.mail != '':
            cur.execute('''SELECT users.id, users.name, secondname, roles.name, code, mail 
                                    FROM users
                                    JOIN roles ON roles.id = users.role_id
                                    JOIN groups ON groups.id = users.group_id
                                    WHERE mail = %s AND password = %s''',
                        (user.mail, user.password))
        else:
            cur.execute('''SELECT users.id, users.name, secondname, roles.name, code, mail
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
                                             'mail': data[5]},
                                              expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                    refresh_token=create_access_token({
                                             'id': data[0],
                                             'role': data[3],
                                             'code': data[4],
                                             'name': data[1],
                                             'secondname': data[2]
                                            }, expires_delta=settings.REFRESH_TOKEN_EXPIRED_HOURS)), True
    except (Exception, psycopg2.DataError) as e:
        return {'Error': str(e)}, False