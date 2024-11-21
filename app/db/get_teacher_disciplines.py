import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.disciplines_model import Disciplines


async def teacher_disciplines(teacher_id: int):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT s.name, g.group_code
        FROM lessons as l
        join public.groups g on g.id = l.group_id
        JOIN public.subjects s on l.subject_id = s.id
        WHERE teacher_id = %s
        ''', (teacher_id,))
        data = cur.fetchall()
        if data is None:
            raise HTTPException(status_code=404, detail='Teacher disciplines not found')
        lessons_and_related_groups = {}
        for subject, group in data:
            if subject not in lessons_and_related_groups:
                lessons_and_related_groups[subject] = []
            lessons_and_related_groups[subject].append(group)

        return Disciplines(lessons_and_related_groups=lessons_and_related_groups)
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f"DB error {e}")
    finally:
        cur.close()
        conn.close()
