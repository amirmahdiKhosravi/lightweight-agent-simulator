import sqlite3
import json
from typing import List, Dict

DB_PATH = "agent_tasks.db"

def init_db():
    """Initializes the SQLite database and creates the tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            final_output TEXT NOT NULL,
            tools_used TEXT NOT NULL,
            execution_steps TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_task(user_input: str, final_output: str, tools_used: List[str], execution_steps: List[str]):
    """Saves a completed task and its trace to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (user_input, final_output, tools_used, execution_steps)
        VALUES (?, ?, ?, ?)
    ''', (user_input, final_output, json.dumps(tools_used), json.dumps(execution_steps)))
    
    conn.commit()
    conn.close()

def get_all_tasks() -> List[Dict]:
    """Retrieves all past tasks, ordered by most recent first."""
    conn = sqlite3.connect(DB_PATH)
    # Return rows as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, user_input, final_output, tools_used, execution_steps, timestamp 
        FROM tasks 
        ORDER BY id DESC
    ''')
    
    rows = cursor.fetchall()
    conn.close()
    
    # Parse the JSON strings back into Python lists for the API response
    tasks = []
    for row in rows:
        tasks.append({
            "id": row["id"],
            "user_input": row["user_input"],
            "final_output": row["final_output"],
            "tools_used": json.loads(row["tools_used"]),
            "execution_steps": json.loads(row["execution_steps"]),
            "timestamp": row["timestamp"]
        })
        
    return tasks
