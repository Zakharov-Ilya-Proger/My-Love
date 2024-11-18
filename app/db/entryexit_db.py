import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.entry_exit import EnExHistory, EnEx, AddEnterExit


async def db_get_person_entrances(person_id, id_column_name, table):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT b.name, b.address, eeh.time, eeh.status 
        FROM %s as eeh
        JOIN public.branches b on eeh.branch_id = b.id 
        WHERE %s = %s''',
                    (table, id_column_name, person_id,))
        data = cur.fetchall()
        if data is None:
            raise HTTPException(status_code=404, detail='No entry/exit history for this person')
        response = EnExHistory(history=[EnEx(
            branch_name=row[0],
            branch_address=row[1],
            time=row[2],
            statuse=row[3]
        ) for row in data])
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()


async def db_post_person_entrances(table, token, en_ex_data: AddEnterExit):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        id_column_name = token['role'] + '_id'
        cur.execute('''
        INSERT INTO %s (%s, branch_id, time, status)
        VALUES (%s, %s, %s, %s)
        ''', (table,
              id_column_name,
              token['id'],
              en_ex_data.branch_id,
              en_ex_data.time,
              en_ex_data.status))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail='No such person or branch')
        raise HTTPException(status_code=200, detail='Enter/exit added')
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()
