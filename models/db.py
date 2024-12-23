import sqlite3
import config

def init_db():
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            cluster TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            name TEXT,
            deadline DATE,
            stress_level INTEGER,
            category TEXT,
            estimated_time INTEGER,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    conn.commit()
    conn.close()



def get_db_connection():
    conn = sqlite3.connect('scheduler.db')
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access for rows
    return conn
