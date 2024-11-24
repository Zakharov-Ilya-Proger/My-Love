import psycopg2
from fastapi import HTTPException

from .config import connector
from ..models.students_on_lesson import StudentsOnLesson


async def add_students_marking(students: StudentsOnLesson):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        for student_id in students.students.keys():
            cur.execute('''
            INSERT INTO attendance 
            (lesson_id, student_id, status) 
            VALUES (%s, %s, %s)
            ''', (students.lesson_id, student_id, students.students[student_id]))
            conn.commit()
        if cur.rowcount == 0:
            return HTTPException(status_code=404, detail='No student was added')
        return HTTPException(status_code=200, detail='Successfully added students.')
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error {e}")
    finally:
        cur.close()
        conn.close()
