import psycopg2
from fastapi import HTTPException

from app.db.config import connector


async def get_enter_token(table, person_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        query = f'''
        SELECT enter_token FROM {table}
        WHERE {table}.id = %s
        '''
        cur.execute(query, (person_id, ))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='Not Found')
        return data[0]
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
