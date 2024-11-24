from datetime import timedelta
import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.db.models import Login, LoggedIn, Reset
from app.pwd_to_hash import check_password, hash_password
from app.tokens import create_access_token


async def check_teacher(user: Login):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        if user.mail is not None:
            cur.execute('''SELECT users.id, users.name, secondname, roles.name, code, mail, lastname, password
                                    FROM teachers as users
                                    JOIN roles ON roles.id = users.role_id
                                    WHERE mail = %s''',
                        (user.mail,))
        else:
            cur.execute('''SELECT users.id, users.name, secondname, roles.name, code, mail, lastname, password
                                    FROM teachers as users
                                    JOIN roles ON roles.id = users.role_id
                                    WHERE phone = %s''',
                        (user.phone,))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='Teacher not found')
        else:
            pwd = data[7]
            if not check_password(user.password, pwd):
                return HTTPException(status_code=401, detail='Incorrect password')
            return LoggedIn(data={
                'id': data[0],
                'name': data[1],
                'secondname': data[2],
                'lastname': data[6],
                'role': data[3],
            },
                access_token=create_access_token({
                    'id': data[0],
                    'role': data[3],
                    'code': data[4],
                    'mail': data[5]},
                    expires_delta=timedelta(minutes=15)),
                refresh_token=create_access_token({
                    'id': data[0],
                    'role': data[3],
                    'code': data[4],
                    'name': data[1],
                    'secondname': data[2],
                    'mail': data[5]
                }, expires_delta=timedelta(days=1)))
    except (Exception, psycopg2.DataError) as e:
        return HTTPException(status_code=500, detail=f'DB Error: {e}')
    finally:
        cur.close()
        conn.close()


async def set_time_code_teacher(mail, random_code):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE teachers SET reset_code = %s WHERE mail = %s''',
                    (random_code, mail))
        if cur.rowcount == 0:
            return HTTPException(status_code=404, detail='User not found')
        else:
            return HTTPException(status_code=200, detail="Success")
    except (Exception, psycopg2.DataError) as e:
        return HTTPException(status_code=500, detail=f'DB Error: {e}')
    finally:
        cur.close()
        conn.commit()
        conn.close()


async def reset_password_teacher(request: Reset):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE teachers SET password = %s WHERE mail = %s AND reset_code = %s''',
                    (hash_password(request.new_password), request.mail, request.reset_code))

        if cur.rowcount == 0:
            return HTTPException(status_code=404, detail='User not found or code is incorrect')
        else:
            return HTTPException(status_code=200, detail="Success")
    except (Exception, psycopg2.DataError) as e:
        return HTTPException(status_code=500, detail=f'DB Error: {e}')
    finally:
        cur.close()
        conn.commit()
        conn.close()
