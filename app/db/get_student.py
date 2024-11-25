import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.student import Student


async def get_student_db(student_code):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT s.id, s.name, secondname, 
        lastname, g.group_code, i.name 
        FROM students as s 
        JOIN public.groups g on s.group_id = g.id
        JOIN public.institutes i on g.institute_id = i.id
        WHERE code = %s 
        ''', (student_code,))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='Student not found')
        return Student(id=data[0],
                       name=data[1],
                       secondname=data[2],
                       lastname=data[3],
                       group=data[4],
                       institute=data[5])
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()


async def get_student_by_token_db(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT s.id, s.name, secondname, 
        lastname, g.group_code, i.name 
        FROM students as s 
        JOIN public.groups g on s.group_id = g.id
        JOIN public.institutes i on g.institute_id = i.id
        WHERE s.id = %s 
        ''', (student_id,))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='Student not found')
        return Student(id=data[0],
                       name=data[1],
                       secondname=data[2],
                       lastname=data[3],
                       group=data[4],
                       institute=data[5])
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()
