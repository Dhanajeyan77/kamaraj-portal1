import sqlite3
import os

if not os.path.exists('database'):
    os.makedirs('database')

def init_db():
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
    )''')

    # FIXED Questions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            content TEXT NOT NULL,      -- Changed from description to content
            solution TEXT NOT NULL,     -- Added missing solution column
            expected_output TEXT NOT NULL
    )''')

    # Attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_roll TEXT NOT NULL,
            question_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            code TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_roll) REFERENCES users(roll_no),
            FOREIGN KEY(question_id) REFERENCES questions(id)
    )''')

    conn.commit()
    conn.close()
    print("✅ Database initialized with correct column names (content and solution).")

if __name__ == "__main__":
    init_db()