import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.entry_exit import EnExHistory, EnEx


async def db_get_student_entrances(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT b.name, b.address, eeh.entry_time, eeh.exit_time, eeh.status FROM entryexithistory as eeh
        JOIN public.branches b on eeh.branch_id = b.id 
        WHERE user_id = %s''',
                    (student_id,))
        data = cur.fetchall()
        if data is None:
            raise HTTPException(status_code=404, detail='No entry/exit history for this user')
        response = EnExHistory(history=[EnEx(
            branch_name=row[0],
            branch_address=row[1],
            entry_time=row[2],
            exit_time=row[3],
            statuse=row[4]
        ) for row in data])
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()
