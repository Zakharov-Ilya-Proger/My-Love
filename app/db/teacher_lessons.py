import psycopg2
from fastapi import HTTPException
from app.models.teacher_lessons import LessonsTeacher, LessonTeacher
from .config import connector


async def get_teacher_lessons(teacher_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT l.id, s.name, group_code, a.name, a.capacity, b.name,
        b.address, start_time, end_time, task, deadline, l.type_of_lesson
        FROM lessons as l
        JOIN public.groups g on l.group_id = g.id
        JOIN public.subjects s on l.subject_id = s.id
        JOIN public.auditories a on l.auditory_id = a.id
        JOIN public.branches as b on a.branch_id = b.id
        JOIN public.tasks t on l.id = t.lesson_id
        WHERE teacher_id = %s
        ''', (teacher_id,))
        data = cur.fetchall()
        if data is None:
            raise HTTPException(status_code=404, detail='No such teacher or this teacher has no lessons')
        response = LessonsTeacher(
            lessons=[
                LessonTeacher(
                    id=row[0],
                    subject=row[1],
                    group=row[2],
                    auditory_name=row[3],
                    auditory_capacity=row[4],
                    branch_name=row[5],
                    branch_address=row[6],
                    start_time=row[7],
                    end_time=row[8],
                    task=row[9],
                    deadline=row[10],
                    type_of_lesson=row[11]
                ) for row in data
            ],
        )
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()
