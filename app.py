from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras
import multiprocessing
import io
import os
from contextlib import redirect_stdout

app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn

def execute_user_code(user_code, expected_answer, result_dict):
    f = io.StringIO()
    try:
        local_vars = {}
        with redirect_stdout(f):
            exec(user_code, {"__builtins__": __builtins__}, local_vars)
        actual_output = f.getvalue().strip()
        expected_output = str(expected_answer).strip()
        result_dict['output'] = actual_output
        result_dict['is_correct'] = actual_output.lower() == expected_output.lower()
    except Exception as e:
        result_dict['error'] = str(e)

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].upper()
        password = request.form["password"]
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE roll_no=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session["user"] = username
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])

@app.route("/questions")
def questions():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM questions ORDER BY date ASC")
    qs = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("questions.html", questions=qs)

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question_detail(qid):
    if "user" not in session:
        return redirect(url_for("login"))
    output = ""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM questions WHERE id=%s", (qid,))
    q = cur.fetchone()

    if request.method == "POST":
        user_code = request.form["user_code"]
        manager = multiprocessing.Manager()
        result_dict = manager.dict()
        p = multiprocessing.Process(target=execute_user_code, args=(user_code, q['expected_output'], result_dict))
        p.start()
        p.join(timeout=3)

        if p.is_alive():
            p.terminate()
            output = "❌ Timeout Error: Infinite loop detected!"
        elif 'error' in result_dict:
            output = f"⚠️ Python Error: {result_dict['error']}"
        else:
            actual = result_dict.get('output', "")
            if result_dict.get('is_correct'):
                output = f"Result: {actual}\n\n✅ CORRECT!"
                cur.execute("""
                    INSERT INTO attempts (user_roll, question_id, status, code)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_roll, question_id)
                    DO UPDATE SET status='Completed', code=EXCLUDED.code, timestamp=CURRENT_TIMESTAMP
                """, (session["user"], qid, "Completed", user_code))
                conn.commit()
            else:
                output = f"Result: {actual}\n\n❌ INCORRECT."
    cur.close()
    conn.close()
    return render_template("question_detail.html", question=q, output=output)

@app.route("/solutions")
def solutions():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Define the roll number from the current session
    current_user_roll = session["user"]
    
    # This query will now work once you run the ALTER TABLE commands above
    cur.execute("""
        SELECT a.code, a.timestamp, q.date, q.content, q.title
        FROM attempts a
        JOIN questions q ON a.question_id = q.id
        WHERE a.user_roll = %s
    """, (current_user_roll,))

    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("solutions.html", solutions=data)

@app.route("/admin/<int:qid>")
def admin_dashboard(qid):
    if "user" not in session:
        return redirect(url_for("login"))
        
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 1. Verify if the logged-in user is an admin
    cur.execute("SELECT is_admin FROM users WHERE roll_no=%s", (session["user"],))
    user = cur.fetchone()

    # PostgreSQL BOOLEAN check (True/False)
    if not user or user['is_admin'] is not True:
        cur.close()
        conn.close()
        return "Access Denied: Admin privileges required.", 403

    # 2. Get the specific question details for the header
    cur.execute("SELECT date, title, content FROM questions WHERE id=%s", (qid,))
    q_info = cur.fetchone()
    
    if not q_info:
        cur.close()
        conn.close()
        return "Question not found", 404

    # 3. Get progress report for all students 
    # FIXED: Added opening parenthesis for (a.timestamp AT TIME ZONE...)
    cur.execute("""
        SELECT 
            u.roll_no, 
            u.name, 
            a.status, 
            (a.timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as timestamp
        FROM users u
        LEFT JOIN attempts a 
            ON u.roll_no = a.user_roll 
            AND a.question_id = %s
        ORDER BY u.roll_no ASC
    """, (qid,))
    
    report = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return render_template("admin.html", report=report, q_info=q_info, qid=qid)
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)