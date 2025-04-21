import sqlite3
import logging

logger = logging.getLogger(__name__)

def setup_todo_app_db():
    """Creates the SQLite database and necessary tables for the to-do app."""
    conn = sqlite3.connect('todo_app.db')
    cursor = conn.cursor()
    
    # Create tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,
        task_description TEXT,
        priority TEXT DEFAULT 'medium',
        status TEXT DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP        
    )
    ''')
    
    conn.commit()
    conn.close()

    logger.info("Database setup completed.")
