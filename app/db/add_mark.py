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
        if cur.rowcount == 0:
            return None, ""
        cur.close()
        conn.commit()
        conn.close()
        return True, ""
    except (Exception, psycopg2.DatabaseError) as e:
        return False, str(e)
