import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.student_est import EstForStudent


async def add_mark_for_student(mark: EstForStudent):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO mark (student_id, lesson_id, mark)  VALUES (%s, %s, %s)''',
                    (mark.student_id, mark.lesson_id, mark.mark))
        if cur.rowcount == 1:
            raise HTTPException(status_code=200, detail='Mark is added')
        else:
            raise HTTPException(status_code=404, detail='No such student or lesson')
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.commit()
        conn.close()
