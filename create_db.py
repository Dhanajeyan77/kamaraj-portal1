import psycopg2

def init_db():
    conn = psycopg2.connect(
        host="db.lgdoppdnlkdrfixxulyb.supabase.co",
        database="postgres",
        user="postgres",
        password="Dhanajeyan@17",
        port=5432,
        sslmode="require"
    )
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

    # QUESTIONS TABLE - Added 'title' to match your schema
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

    # ATTEMPTS TABLE - Using 'timestamp' and adding UNIQUE constraint for ON CONFLICT
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
    print("✅ PostgreSQL database initialized successfully.")

if __name__ == "__main__":
    init_db()