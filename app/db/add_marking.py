import psycopg2
from fastapi import HTTPException

from .config import connector
from ..models.students_on_lesson import StudentsOnLesson


async def add_students_marking(students: StudentsOnLesson):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        for student_id in students.students_id:
            cur.execute('''
            INSERT INTO attendance 
            (lesson_id, student_id, check_in_time, check_out_time, status) 
            VALUES (%s, %s, %s, %s, %s)
            ''', (students.lesson_id, student_id, students.check_in_time, students.check_out_time, students.status))
        if cur.rowcount != len(students.students_id):
            raise HTTPException(status_code=404, detail='Students/student or lesson not found')
        conn.commit()
        raise HTTPException(status_code=200, detail='Students are successfully added')
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'Something went wrong: {e}')
    finally:
        cur.close()
        conn.close()
