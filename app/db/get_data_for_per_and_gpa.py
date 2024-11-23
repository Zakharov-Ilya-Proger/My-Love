import psycopg2
from app.db.config import connector


async def get_data_for_gpa(student_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT SUM(gpa) from (SELECT avg(mark.mark) * s.duration /
       (SELECT SUM(unique_subjects.duration)
             FROM (
                 SELECT DISTINCT s2.name, s2.duration
                 FROM public.mark m2
                 JOIN public.lessons l2 ON l2.id = m2.lesson_id
                 JOIN public.subjects s2 ON s2.id = l2.subject_id
                 WHERE m2.student_id = %s
             ) AS unique_subjects) as gpa
        FROM mark
                 JOIN public.lessons l on mark.lesson_id = l.id
                JOIN public.subjects s on s.id = l.subject_id
        WHERE student_id = %s
        GROUP BY s.name, s.duration) as mlsg
        ''', (student_id, student_id))
        data = cur.fetchone()
        if data is None:
            return None, None
        return float(round(data[0], 3)), True
    except (Exception, psycopg2.DatabaseError) as e:
        return e, False
    finally:
        cur.close()
        conn.close()

async def count_percentile_from_db():
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT
            SUM(CASE WHEN gpa > avg_gpa THEN 1 ELSE 0 END)::FLOAT / COUNT(*) * 100 AS ratio_above_average
        FROM (
            SELECT calculate_gpa(s.id) AS gpa,
                   (SELECT AVG(calculate_gpa(s2.id)) FROM students s2) AS avg_gpa
            FROM students AS s
        ) AS all_s_gpa; 
        ''')
        data = cur.fetchone()
        if data is None:
            return None, None
        return f"{round(data[0], 3)}%", True
    except (Exception, psycopg2.DatabaseError) as e:
        return e, False
    finally:
        cur.close()
        conn.close()
