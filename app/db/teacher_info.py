import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.teacher import Teacher


async def get_teacher_info_db(teacher_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT t.name, t.secondname, t.lastname, 
        t.code, d.name, i.name 
        FROM teachers as t
        JOIN public.department d on t.department_id = d.id
        JOIN public.institutes i on d.institute_id = i.id
        WHERE t.id = %s
        ''', (teacher_id, ))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='Teacher not found')
        name, secondname, lastname, code, d_name, i_name = data
        cur.execute('''
        SELECT s.name FROM lessons as l 
        JOIN public.subjects s on s.id = l.subject_id
        WHERE l.teacher_id = %s
        ''', (teacher_id, ))
        sub = cur.fetchall()
        subjects = []
        for s in sub:
            if s not in subjects:
                subjects.append(s[0])
        subjects = None if len(subjects) == 0 else subjects
        return Teacher(name=name,
                       secondname=secondname,
                       lastname=lastname,
                       code=code,
                       dep_name=d_name,
                       institute=name,
                       subjects=subjects
                       )
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=404, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()
