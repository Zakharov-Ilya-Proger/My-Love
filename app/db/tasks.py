import psycopg2
from fastapi import HTTPException
from psycopg2 import errors
from app.db.config import connector
from app.models.lesson import Task


async def add_task_to_db(task: Task):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        INSERT INTO tasks (lesson_id, task, deadline) VALUES (%s, %s, %s) 
        ''', (task.lesson_id, task.task, task.deadline))
        conn.commit()
        if cur.rowcount == 1:
            return HTTPException(status_code=200, detail="Success")
        return HTTPException(status_code=404, detail="Fail")
    except errors.UniqueViolation:
        conn.rollback()
        return HTTPException(status_code=409, detail="Fail")
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        return HTTPException(status_code=500, detail=f"DB error: {error}")
    finally:
        cur.close()
        conn.close()


async def update_task_from_db(task: Task):
    conn = psycopg2.connect(**connector)
    cur = conn.cursor()
    try:
        cur.execute('''
        UPDATE tasks as t SET task = %s, deadline = %s WHERE lesson_id = %s 
        ''', (task.task, task.deadline, task.lesson_id))
        conn.commit()
        if cur.rowcount == 1:
            return HTTPException(status_code=200, detail="Success")
        return HTTPException(status_code=404, detail="Fail")
    except (Exception, psycopg2.DatabaseError) as error:
        conn.rollback()
        return HTTPException(status_code=500, detail=f"DB error: {error}")
    finally:
        cur.close()
        conn.close()
