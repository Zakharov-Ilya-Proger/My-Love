import psycopg2
from fastapi import HTTPException
from app.db.config import connector
from app.models.access_control import AccessControl


async def check_access_to_auditory_db(table_name, id_name, access: AccessControl, per_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        query = f'''
        SELECT  type, id
        FROM accesscontrol_{table_name}
        WHERE {id_name} = %s
        AND
        %s > access_start_time 
        AND
        %s < access_start_time + INTERVAL '1.5 hours'
        '''
        cur.execute(query, (per_id, access.time, access.time))
        data = cur.fetchone()
        if data is None:
            return HTTPException(status_code=404, detail='Access Denied')
        query = f'''
        INSERT INTO accesshistory_{table_name}
        ({id_name}, auditory_id, access_start_time, access_type, reason, control)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cur.execute(query, (per_id, access.audit_id, access.time, data[0], access.reason, data[1]))
        conn.commit()
        if cur.rowcount == 0:
            return HTTPException(status_code=409, detail='Control denied')
        return HTTPException(status_code=201, detail='Control added successfully')
    except (Exception, psycopg2.DatabaseError) as error:
        return HTTPException(status_code=500, detail=f"DB error: {error}")
    finally:
        cur.close()
        conn.close()
