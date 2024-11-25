import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.group import Group, StudentInfo


async def get_group_db(group_code):
    conn = psycopg2.connect(**connector)
    cur = await conn.cursor()
    try:
        cur.execute('''
        SELECT s.id, s.name, s.secondname, s.lastname, s.code
        FROM students as s
        JOIN public.groups g on g.id = s.group_id
        WHERE group_code = %s
        ''')
        data = cur.fetchall()
        if data is None:
            return HTTPException(status_code=404, detail='Group not found')
        response = Group(group_code=group_code,
                         group=[StudentInfo(
                             id=row[0],
                             name=row[1],
                             secondname=row[2],
                             lastname=row[3],
                             code=row[4])
                             for row in data])
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()
