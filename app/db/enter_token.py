import psycopg2
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
            return None, None
        return True, data[0]
    except (Exception, psycopg2.DatabaseError) as e:
        return False, e