from .db import get_db_connection
from .scheduling_pipeline import generate_schedule
import datetime

def save_task(user_email, task):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (user_email, name, deadline, stress_level, category, estimated_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_email, task['name'], task['deadline'], task['stress_level'], task['category'], task['estimated_time']))
    conn.commit()
    conn.close()

def get_tasks_due_today_or_nearest(user_email):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Step 1: Check if there are tasks due today
    cursor.execute('SELECT * FROM tasks WHERE user_email = ? AND date(deadline) = date("now")', (user_email,))
    tasks = cursor.fetchall()
    
    # Step 2: If no tasks due today, find the tasks with the nearest future deadline
    if not tasks:
        cursor.execute('''
            SELECT * FROM tasks 
            WHERE user_email = ? AND date(deadline) > date("now")
            ORDER BY date(deadline) ASC
            LIMIT 1
        ''', (user_email,))
        
        nearest_deadline_task = cursor.fetchone()
        
        # Step 3: If a nearest deadline task is found, retrieve all tasks for that date
        if nearest_deadline_task:
            nearest_deadline = nearest_deadline_task["deadline"]
            cursor.execute('SELECT * FROM tasks WHERE user_email = ? AND date(deadline) = ?', (user_email, nearest_deadline))
            tasks = cursor.fetchall()

    conn.close()
    return [map_task_to_dict(task) for task in tasks]

def map_task_to_dict(task_row):
    """
    Maps a database row to the task dictionary format expected by the ML pipeline.
    """
    return {
        'name': task_row['name'],
        'category': task_row['category'],
        'stress_level': task_row['stress_level'],
        'estimated_time': task_row['estimated_time'],
        'deadline': task_row['deadline']
    }

def generate_personalized_schedule(user_email, user_profile):
    tasks = get_tasks_due_today_or_nearest(user_email)
    return generate_schedule(tasks, user_profile)
