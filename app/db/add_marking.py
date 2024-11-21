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
        print(cur.rowcount)
        if cur.rowcount == 0:
            return None
        return True
    except (Exception, psycopg2.DatabaseError) as e:
        return e
    finally:
        cur.close()
        conn.close()
