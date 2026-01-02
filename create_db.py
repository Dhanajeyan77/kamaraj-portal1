import os
import psycopg2

def init_db():
    # 1. Get the Neon URL from the terminal environment
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL is not set. Run 'export DATABASE_URL=...' in terminal first.")
        return

    try:
        # 2. Connect using the URL string only
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # USERS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                roll_no TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE
            );
        """)

        # QUESTIONS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                content TEXT NOT NULL,
                solution TEXT NOT NULL,
                expected_output TEXT NOT NULL
            );
        """)

        # ATTEMPTS TABLE
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id SERIAL PRIMARY KEY,
                user_roll TEXT NOT NULL REFERENCES users(roll_no),
                question_id INTEGER NOT NULL REFERENCES questions(id),
                status TEXT,
                code TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_roll, question_id)
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Neon database initialized successfully with all tables.")

    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    init_db()