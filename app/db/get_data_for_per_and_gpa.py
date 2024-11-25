import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.Statist import GPA, Percentile


async def get_data_for_gpa(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT * FROM calculate_gpa(%s)
        ''', (student_id,))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='No data found')
        return GPA(gpa=data[0])
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()

async def count_percentile_from_db(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT
            SUM(CASE WHEN gpa > calculate_gpa(%s) THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 AS ratio_above_average
        FROM (
            SELECT calculate_gpa(s.id) AS gpa,
                   (SELECT AVG(calculate_gpa(s2.id)) FROM students s2) AS avg_gpa
            FROM students AS s
        ) AS all_s_gpa; 
        ''', (student_id,))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='No data found')
        return Percentile(percentile=round(data[0], 3))
    except (Exception, psycopg2.DatabaseError) as e:
        return HTTPException(status_code=500, detail=f"DB error: {e}")
    finally:
        cur.close()
        conn.close()
