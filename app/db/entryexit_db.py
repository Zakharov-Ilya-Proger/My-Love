import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.entry_exit import EnExHistory, EnEx


async def db_get_person_entrances(person_id, id_column_name, table):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        query = f'''
                SELECT b.name, b.address, eeh.time, eeh.status
                FROM {table} as eeh
                JOIN public.branches b on eeh.branch_id = b.id
                WHERE {id_column_name} = %s
                '''
        cur.execute(query, (person_id,))
        data = cur.fetchall()
        if data is None:
            return HTTPException(status_code=404, detail='No entry/exit history for this person')
        response = EnExHistory(root=[EnEx(
            branch_name=row[0],
            branch_address=row[1],
            time=row[2],
            status=row[3]
        ) for row in data])
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f'DB error in entry exit {e}')
    finally:
        cur.close()
        conn.close()
