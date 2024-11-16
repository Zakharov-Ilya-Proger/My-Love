from fastapi import HTTPException

import psycopg2

from app.db.config import connector
from app.models.group_info import StudentGroupInfo, GroupInfo


async def get_groups_db(teacher_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        SELECT g.group_code, s.name, s.secondname, s.lastname, s.code, s.id FROM lessons
        JOIN public.groups g on g.id = lessons.group_id
        JOIN public.students s on g.id = s.group_id
        WHERE teacher_id = %s
        ORDER BY group_code
        ''',(teacher_id,))

        rows = cur.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="No such teacher or this teacher has no lessons")
        result = GroupInfo()
        for row in rows:
            group_code = row[0]
            student_info = StudentGroupInfo(name=row[1],secondname=row[2], lastname=row[3], code=row[4], id=row[5])
            if group_code not in result:
                result.groups[group_code] = []
            result.groups[group_code].append(student_info)

        return result
    except (Exception, psycopg2.DatabaseError) as e:
        raise HTTPException(status_code=500, detail=f'DB error {e}')
    finally:
        cur.close()
        conn.close()
