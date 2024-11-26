import psycopg2
from fastapi import HTTPException

from app.db.config import connector
from app.models.access_control import CloseAccess


async def close_access_to_auditory_db(table_name, id_name, access: CloseAccess, per_id):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        query = f'''
        UPDATE accesshistory_{table_name}
        SET access_end_time = %s
        WHERE {id_name} = %s AND auditory_id = %s
        AND %s < access_start_time + INTERVAL '1.63 hours'
        '''
        cur.execute(query, (access.time, per_id, access.audit_id, access.time))
        conn.commit()
        if cur.rowcount == 0:
            return HTTPException(status_code=404, detail='No auditory data found')
        return HTTPException(status_code=200, detail='Auditory data was closed')
    except (Exception, psycopg2.DatabaseError) as error:
        return HTTPException(status_code=500, detail=f"DB error: {error}")
    finally:
        cur.close()
        conn.close()
