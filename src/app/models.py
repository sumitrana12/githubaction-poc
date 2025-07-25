import sqlite3
import os
from datetime import datetime
from app import app, logger

def get_db_connection():
    db_path = os.path.join(os.getenv('DB_PATH', './data'), 'database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database initialized")

def get_messages():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY created_at DESC').fetchall()
    conn.close()
    return [{
        "id": row['id'],
        "content": row['content'],
        "created_at": row['created_at']
    } for row in messages]

def add_message(content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (content) VALUES (?)', (content,))
    conn.commit()
    message_id = cursor.lastrowid
    conn.close()
    
    return {
        "id": message_id,
        "content": content,
        "created_at": datetime.now().isoformat()
    } 