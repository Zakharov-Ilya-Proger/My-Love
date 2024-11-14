import psycopg2

from app.models.reset import Reset
from config import connector

async def set_time_code(user_id, random_code):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE users SET reset_code = %s WHERE id = %s''',
                    (random_code, user_id))
        cur.close()
        conn.commit()
        conn.close()
        if cur.rowcount == 0:
            return False
        else:
            return True
    except (Exception, psycopg2.DataError) as e:
        return e


async def reset_password(user_id, request: Reset):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''UPDATE users SET password = %s WHERE id = %s AND reset_code = %s''',
                    (request.password, user_id, request.reset_code))
        cur.close()
        conn.commit()
        conn.close()
        if cur.rowcount == 0:
            return False
        else:
            return True
    except (Exception, psycopg2.DataError) as e:
        return e