import sqlite3

def init_db():
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            task_type TEXT,
            estimated_time INTEGER,
            stress_level INTEGER,
            priority INTEGER,
            urgency INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def save_task(user_id, task_type, estimated_time, stress_level, priority, urgency):
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (user_id, task_type, estimated_time, stress_level, priority, urgency)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, task_type, estimated_time, stress_level, priority, urgency))
    conn.commit()
    conn.close()

def get_tasks(user_id):
    conn = sqlite3.connect('scheduler.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks
