import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.custom_lessons import CustomLessons, CustomLessonForStudent


async def add_custom_lesson_db(lesson, student):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT start_time, end_time, name  FROM lessons
        JOIN subjects s on lessons.subject_id = s.id
        JOIN public.groups g on lessons.group_id = g.id
        WHERE group_code = %s AND 
        EXTRACT(DAY FROM start_time) = %s
        ORDER BY start_time 
        ''', (student['group'], lesson.start_time.day))
        data = cur.fetchall()
        string_of_proeb = "Задетые пары: "
        lessons = []
        for start, end, name in data:
            if start <= lesson.start_time <= end or start <= lesson.end_time <= end:
                lessons.append(f"{name} [{start}/{end}]")
        if len(lessons) != 0:
            return HTTPException(status_code=418, detail=string_of_proeb + ', '.join(lessons))
        cur.execute('''
        INSERT INTO custom_lessons 
        (name, start_time, end_time, auditory_id, student_id)
        VALUES (%s, %s, %s, %s, %s)
        ''', (lesson.name, lesson.start_time, lesson.end_time,
              lesson.auditory_id, student['id']))
        conn.commit()
        return HTTPException(status_code=200, detail="Success")
    except (Exception, psycopg2.DatabaseError) as error:
        return HTTPException(status_code=500, detail=f"DB error: {error}")
    finally:
        cur.close()
        conn.close()


async def get_custom_lessons_db(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT cl.name, cl.start_time, cl.end_time, a.name, b.address, b.name
        FROM custom_lessons as cl
        LEFT JOIN auditories AS a ON cl.auditory_id = a.id
        LEFT JOIN public.branches b on a.branch_id = b.id
        WHERE cl.student_id = %s
        ''', (student_id,))
        data = cur.fetchall()
        if data is None:
            return HTTPException(status_code=404, detail="Not Found")
        response = [
            CustomLessonForStudent(name=row[0],
                                   start_time=row[1],
                                   end_time=row[2],
                                   auditory=row[3],
                                   address=None if row[4] is None
                                                   and row[5] is None
                                   else str(row[5]) + " " + str(row[4]))
            for row in data]
        return CustomLessons(custom_lessons=response)
    except (Exception, psycopg2.DatabaseError) as error:
        return HTTPException(status_code=500, detail=f"DB error: {error}")
    finally:
        cur.close()
        conn.close()
