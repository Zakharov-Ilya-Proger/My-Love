import psycopg2
from fastapi import HTTPException
from psycopg2 import errors

from app.db.config import connector
from app.models.barrier_model import AddEnterExit


async def db_post_person_entrances(table, token, column, en_ex_data: AddEnterExit):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        # Проверка на существование branch_id
        check_query = f'''
        SELECT 1 FROM branches WHERE id = %s
        '''
        cur.execute(check_query, (en_ex_data.branch_id,))
        if cur.fetchone() is None:
            return HTTPException(status_code=404, detail='No such branch')
        query = f'''
        INSERT INTO {table} ({column}, branch_id, time, status)
        VALUES (%s, %s, %s, %s)
        '''
        cur.execute(query, (
              token['role_id'],
              en_ex_data.branch_id,
              en_ex_data.time,
              en_ex_data.status))
        conn.commit()
        if cur.rowcount == 0:
            return HTTPException(status_code=404, detail='No such person or branch')
        return HTTPException(status_code=200, detail='Enter/exit added')
    except errors.ForeignKeyViolation:
        conn.rollback()
        return HTTPException(status_code=409, detail="Fail")
    except (Exception, psycopg2.DatabaseError) as e:
        conn.rollback()
        return HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()

