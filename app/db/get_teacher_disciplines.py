import psycopg2
from fastapi import HTTPException

from .config import connector
from ..models.disciplines_model import Disciplines


async def teacher_disciplines(teacher_id):
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
        response = Disciplines()
        for subject, group in data:
            if subject not in response:
                response.lessons_and_related_groups[subject] = []
            response.lessons_and_related_groups[subject].append(group)
        return response
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f"DB error {e}")
    finally:
        cur.close()
        conn.close()
