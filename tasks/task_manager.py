from .db import get_db_connection
from .scheduling_pipeline import generate_schedule

def save_task(user_email, task):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (user_email, name, deadline, stress_level, category, estimated_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_email, task['name'], task['deadline'], task['stress_level'], task['category'], task['estimated_time']))
    conn.commit()
    conn.close()

def get_tasks_due_today(user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_email = ? AND date(deadline) = date("now")', (user_email,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def generate_personalized_schedule(user_email, user_profile):
    tasks = get_tasks_due_today(user_email)
    return generate_schedule(tasks, user_profile)
