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
    """ create tasks and users tables if not exists """
    conn = create_connection()
    with conn:
        sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        email text NOT NULL UNIQUE
                                    );"""
        conn.execute(sql_create_users_table)

        sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                        id integer PRIMARY KEY,
                                        title text NOT NULL,
                                        description text,
                                        completed boolean NOT NULL CHECK (completed IN (0, 1)),
                                        due_date text,
                                        user_id integer NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id)
                                    );"""
        conn.execute(sql_create_tasks_table)


def get_tasks(user_id):
    """ fetch all tasks for a specific user from the database """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    tasks = [dict(id=row[0], title=row[1], description=row[2], completed=bool(row[3]), due_date=row[4]) for row in rows]
    return tasks


def add_task(task, user_id):
    """ add a new task for a specific user to the database """
    conn = create_connection()
    sql = ''' INSERT INTO tasks(title, description, completed, due_date, user_id)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (task['title'], task['description'], task['completed'], task['due_date'], user_id))
    conn.commit()
    return cur.lastrowid


def update_task(task_id, task, user_id):
    """ update an existing task for a specific user in the database """
    conn = create_connection()
    sql = ''' UPDATE tasks
              SET title = ?,
                  description = ?,
                  completed = ?,
                  due_date = ?
              WHERE id = ? AND user_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (task['title'], task['description'], task['completed'], task['due_date'], task_id, user_id))
    conn.commit()


def delete_task(task_id, user_id):
    """ delete a task for a specific user from the database """
    conn = create_connection()
    sql = 'DELETE FROM tasks WHERE id = ? AND user_id = ?'
    cur = conn.cursor()
    cur.execute(sql, (task_id, user_id))
    conn.commit()


def get_user_by_email(email):
    """ fetch a user by email from the database """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    return user


def add_user(email):
    """ add a new user to the database """
    conn = create_connection()
    sql = ''' INSERT INTO users(email)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (email,))
    conn.commit()
    return cur.lastrowid
