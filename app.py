import os
import json
import psycopg2
import psycopg2.extras
import pytz
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from psycopg2 import pool

# 🔥 INTERNAL MODULES
from test_cases_data import TEST_CASES_DICT  # Local test cases to prevent DB lag
from queue_worker import submit_job, get_result # The NsJail synchronized worker

# ==========================================
# 1. INITIALIZATION & CONFIGURATION
# ==========================================
load_dotenv()
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

DATABASE_URL = os.environ.get("DATABASE_URL")
db_pool = None

def init_pool():
    global db_pool
    try:
        # High keepalives protect against Neon DB SSL timeouts during the exam
        db_pool = psycopg2.pool.ThreadedConnectionPool(
            5, 50,
            dsn=DATABASE_URL,
            sslmode="require",
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
    except Exception as e:
        print("DB INITIALIZATION ERROR:", e)
        db_pool = None

init_pool()

def get_db_connection():
    global db_pool
    if db_pool is None:
        init_pool()
    
    conn = None
    try:
        conn = db_pool.getconn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
        return conn
    except (psycopg2.OperationalError, psycopg2.InterfaceError, Exception):
        if conn and db_pool:
            db_pool.putconn(conn, close=True)
        init_pool()
        return db_pool.getconn()

def release_db_connection(conn):
    if db_pool and conn:
        try:
            db_pool.putconn(conn)
        except Exception:
            pass

# ==========================================
# 2. ROUTES
# ==========================================

@app.route("/")
def index():
    return redirect(url_for("home")) if "user" in session else redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].upper()
        password = request.form["password"]
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM users WHERE roll_no=%s AND password=%s", (username, password))
            user = cur.fetchone()
            if user:
                session["user"] = username
                session["is_admin"] = user.get("is_admin", False)
                return redirect(url_for("home"))
        finally:
            release_db_connection(conn)
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
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM questions ORDER BY id ASC")
        qs = cur.fetchall()
    finally:
        release_db_connection(conn)
    return render_template("questions.html", questions=qs)

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question_detail(qid):
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    output = ""
    user_code = ""

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM questions WHERE id=%s", (qid,))
        question = cur.fetchone()

        test_cases = TEST_CASES_DICT.get(qid, [])

        if request.method == "POST":
            user_code = request.form["user_code"]
            language = request.form.get("lang_choice", "python")

            job_id = submit_job(user=session["user"], code=user_code, language=language, test_cases=test_cases)
            result = get_result(job_id)

            # Re-check DB connection stability
            try:
                cur.execute("SELECT 1")
            except:
                conn = get_db_connection()
                cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 🔥 SAFE DATA EXTRACTION
            test_results = result.get("test_results") or []
            total_cases = len(test_results)
            passed_cases = sum(1 for r in test_results if r.get("passed"))

            if result.get("all_passed"):
                output = f"✅ SUCCESS: {passed_cases}/{total_cases} Test Cases Passed!"
                # ... (Success Database Logic remains unchanged) ...
                conn.commit()
            else:
                # SAFE SEARCH: Locate the first failure
                failed_test = next((r for r in test_results if not r.get("passed")), None)
                
                if failed_test:
                    output = f"❌ FAILED: {passed_cases}/{total_cases} Passed\n"
                    output += f"---------------------------\n"
                    output += f"Test Case Failed: Input was '{failed_test.get('input', 'N/A')}'\n"
                    output += f"Expected Output:   {failed_test.get('expected', 'N/A')}\n"
                    output += f"Your Output:       {failed_test.get('actual', 'N/A')}\n"
                    
                    # 🔥 FIXED: Check for NoneType before .get()
                    error_msg = failed_test.get('error')
                    if error_msg and isinstance(error_msg, str) and "STANDALONE" not in error_msg:
                        output += f"\nError Message: {error_msg}"
                else:
                    # Fallback for system-level kills
                    output = "❌ ERROR: Execution was terminated (Time/Memory Limit Exceeded)."

    finally:
        release_db_connection(conn)

    return render_template("question_detail.html", question=question, output=output, user_code=user_code)

@app.route("/leaderboard")
def leaderboard():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT username, COUNT(DISTINCT problem_id) total
            FROM submissions WHERE status='Success'
            GROUP BY username ORDER BY total DESC
        """)
        rankings = cur.fetchall()
    finally:
        release_db_connection(conn)
    return render_template("leaderboard.html", rankings=rankings)

@app.route("/solutions")
def solutions():
    if "user" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("""
            SELECT s.status, s.created_at, s.language, q.title, q.date, a.code
            FROM submissions s 
            JOIN questions q ON s.problem_id = q.id 
            LEFT JOIN attempts a ON s.username = a.user_roll 
                AND s.problem_id = a.question_id 
                AND s.language = a.language
            WHERE s.username = %s AND s.status = 'Success'
            ORDER BY s.created_at DESC
        """, (session["user"],))
        user_solutions = cur.fetchall()
    finally: 
        release_db_connection(conn)
    return render_template("solutions.html", solutions=user_solutions)

from datetime import datetime
import pytz

# Define IST for accurate submission tracking in Kamaraj College
IST = pytz.timezone('Asia/Kolkata')

@app.route("/admin")
@app.route("/admin/<int:qid>")
def admin(qid=None):
    """
    Main Admin Dashboard.
    Supports historical date selection starting from Dec 24, 2025.
    """
    if not session.get("is_admin"): 
        return redirect(url_for("home"))
    
    # 1. Capture today's date or the date picked by the teacher
    today_str = datetime.now(IST).strftime('%Y-%m-%d')
    selected_date = request.args.get('date', today_str) 
    
    conn = get_db_connection()
    q_info = None

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 2. Query Question Info for the chosen date
        cur.execute("SELECT id, title, date FROM questions WHERE date = %s LIMIT 1", (selected_date,))
        q_info = cur.fetchone()

        # 3. Fallback Logic: Prevents crashes if no question is assigned to a date
        if not q_info:
            # Fallback to provided QID or the first problem
            qid = qid or 1
            cur.execute("SELECT id, title, date FROM questions WHERE id = %s", (qid,))
            q_info = cur.fetchone()
        else:
            qid = q_info['id']

        # 4. Fetch Student Status Report
        # Filters WHERE u.flag = 0 to exclude yourself and the teacher from the list.
          # --- Updated Query in app.py ---
        cur.execute("""
        SELECT u.roll_no, u.name, 
           COALESCE(latest_a.status, 'Pending') as status,
           latest_a.timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata' as timestamp
        FROM users u 
        LEFT JOIN (
        -- This subquery picks ONLY the latest attempt per student per question
        SELECT DISTINCT ON (user_roll, question_id) 
               user_roll, status, timestamp 
        FROM attempts 
        WHERE question_id = %s
        ORDER BY user_roll, question_id, timestamp DESC
        ) latest_a ON u.roll_no = latest_a.user_roll
        WHERE u.flag = 0 
        ORDER BY u.roll_no ASC
        """, (qid,))
        report = cur.fetchall()
        
    finally: 
        release_db_connection(conn)

    # Return all variables needed for the template
    return render_template(
        "admin.html", 
        report=report, 
        q_info=q_info, 
        qid=qid, 
        selected_date=selected_date
    )


@app.route("/admin/track/<user>")
def admin_track(user):
    """
    User Deep Dive & Activity Heatmap.
    Tracks unique problems solved from Dec 2025 through 2026.
    """
    if not session.get("is_admin"): 
        return redirect(url_for("home"))
        
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Fetch total unique successful solves (source for problem list)
        cur.execute("""
            SELECT DISTINCT problem_id 
            FROM submissions 
            WHERE username = %s AND status = 'Success'
        """, (user,))
        solved = [row['problem_id'] for row in cur.fetchall()]
        
        # 2. Generate Heatmap Data
        # Uses COUNT(DISTINCT problem_id) to ensure students are only credited 
        # for NEW solves each day, ignoring duplicate resubmissions.
        cur.execute("""
            SELECT DATE(created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as date, 
                   COUNT(DISTINCT problem_id) as count
            FROM submissions 
            WHERE username = %s AND status = 'Success' 
            GROUP BY date
        """, (user,))
        heatmap = {str(row['date']): row['count'] for row in cur.fetchall()}
        
    finally: 
        release_db_connection(conn)
        
    return render_template(
        "admin_use_detail.html", 
        user=user, 
        solved=solved, 
        heatmap=heatmap
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==========================================
if __name__ == "__main__":
    # Ensure port 10000 is open on your Ubuntu laptop firewall
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)), debug=False)