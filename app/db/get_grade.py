import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.grade import StudentGrade, StudentGradesInGroup, TeacherGrade


async def grade_for_student(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT s.name, m.mark from mark as m
        JOIN public.lessons l on m.lesson_id = l.id
        JOIN public.subjects s on l.subject_id = s.id
        WHERE student_id = %s
        ''', (student_id,))
        data = cur.fetchall()
        if data is None:
            return HTTPException(status_code=404, detail='Student not found')
        dicted_data = {}
        for name, mark in data:
            if name not in dicted_data:
                dicted_data[name] = []
            dicted_data[name].append(mark)
        return StudentGrade(subjects=dicted_data)
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error {e}")
    finally:
        cur.close()
        conn.close()


async def get_students_grade_for_teacher(teacher_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT group_code, m.mark, s.name, s.secondname, s.lastname, s2.name FROM mark as m 
        JOIN public.lessons l on m.lesson_id = l.id
        JOIN public.students s on m.student_id = s.id
        JOIN public.groups g on s.group_id = g.id
        JOIN public.subjects s2 on l.subject_id = s2.id
        WHERE l.teacher_id = %s
        ''', (teacher_id,))
        data = cur.fetchall()
        if data is None:
            return HTTPException(status_code=404, detail='Teacher not found')
        groups_data = {}
        for group_code, mark, name, secondname, lastname, subject_name in data:
            FIO = f"{name} {secondname} {lastname}"
            student_grade = StudentGradesInGroup(FIO=FIO, marks=mark, subjects=subject_name)
            if group_code not in groups_data:
                groups_data[group_code] = []
            groups_data[group_code].append(student_grade)
        return TeacherGrade(groups=groups_data)
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error {e}")
    finally:
        cur.close()
        conn.close()
