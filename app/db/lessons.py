import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.lesson import Lessons, Lesson


async def get_lessons_from_db(group):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT l.id, s.name, g.group_code, a.name, a.capacity, b.name, b.address, 
            l.start_time, l.end_time, u.name, u.secondname, u.lastname, t.task, t.deadline, l.type_of_lesson
            FROM lessons as l
            JOIN public.auditories a on a.id = l.auditory_id
            JOIN public.subjects s on s.id = l.subject_id
            JOIN public.branches b on b.id = a.branch_id
            JOIN public.groups g on g.id = l.group_id
            JOIN public.teachers u on u.id = l.teacher_id
            LEFT JOIN public.tasks t on l.id = t.lesson_id
        WHERE g.group_code = %s
        ORDER BY l.start_time
        ''', (group,))
        data = cur.fetchall()
        if data is None:
            return HTTPException(status_code=404, detail="No lessons for this group")
        return Lessons(root=
        [Lesson(
            id=row[0],
            subject=row[1], group=row[2],
            auditory_name=row[3], auditory_capacity=row[4],
            branch_name=row[5], branch_address=row[6],
            start_time=row[7], end_time=row[8],
            teacher_name=row[9], teacher_secondname=row[10],
            teacher_lastname=row[11], task=row[12],
            deadline=row[13], type_of_lesson=row[14])
            for row in data])
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f'DB error {e}')


async def get_lesson_from_lesson_id_db(lesson_id: int):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT l.id, s.name, g.group_code, a.name, a.capacity, b.name, b.address,
            l.start_time, l.end_time, u.name, u.secondname, u.lastname, t.task, t.deadline, l.type_of_lesson
            FROM lessons as l
            JOIN public.auditories a on a.id = l.auditory_id
            JOIN public.subjects s on s.id = l.subject_id
            JOIN public.branches b on b.id = a.branch_id
            JOIN public.groups g on g.id = l.group_id
            JOIN public.teachers u on u.id = l.teacher_id
            JOIN public.tasks t on l.id = t.lesson_id
            WHERE l.id = %s
            ''', (lesson_id,))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail="No lesson found with the given ID")
        else:
            return Lesson(id=data[0], subject=data[1],
                          group=data[2], auditory_name=data[3],
                          auditory_capacity=data[4], branch_name=data[5],
                          branch_address=data[6], start_time=data[7],
                          end_time=data[8], teacher_name=data[9],
                          teacher_secondname=data[10], teacher_lastname=data[11],
                          task=data[12], deadline=data[13], type_of_lesson=data[14])
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()