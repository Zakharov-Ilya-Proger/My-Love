

import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.reset import Reset

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