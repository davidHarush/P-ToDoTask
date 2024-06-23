import sqlite3
from sqlite3 import Error

DATABASE = 'tasks.db'

def create_connection():
    """ create a database connection to the SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
    except Error as e:
        print(e)
    return conn

def init_db():
    """ create tasks table if not exists """
    conn = create_connection()
    with conn:
        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        description text,
                                        completed boolean NOT NULL CHECK (completed IN (0, 1)),
                                        due_date text
                                    );"""
        conn.execute(sql_create_tasks_table)

def get_tasks():
    """ fetch all tasks from the database """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    tasks = [dict(id=row[0], title=row[1], description=row[2], completed=bool(row[3]), due_date=row[4]) for row in rows]
    return tasks

def add_task(task):
    """ add a new task to the database """
    conn = create_connection()
    sql = ''' INSERT INTO tasks(title, description, completed, due_date)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (task['title'], task['description'], task['completed'], task['due_date']))
    conn.commit()
    return cur.lastrowid

def update_task(task_id, task):
    """ update an existing task in the database """
    conn = create_connection()
    sql = ''' UPDATE tasks
              SET title = ?,
                  description = ?,
                  completed = ?,
                  due_date = ?
              WHERE id = ? '''
    cur = conn.cursor()
    cur.execute(sql, (task['title'], task['description'], task['completed'], task['due_date'], task_id))
    conn.commit()

def delete_task(task_id):
    """ delete a task from the database """
    conn = create_connection()
    sql = 'DELETE FROM tasks WHERE id = ?'
    cur = conn.cursor()
    cur.execute(sql, (task_id,))
    conn.commit()
