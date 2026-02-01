import re
import os
import json
import psycopg2
import psycopg2.extras
import pytz
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
from psycopg2 import pool
from werkzeug.middleware.proxy_fix import ProxyFix

# 🔥 INTERNAL MODULES
from test_cases_data import TEST_CASES_DICT  
from queue_worker import submit_job, get_result 

# ==========================================
# 1. INITIALIZATION & CONFIGURATION
# ==========================================
load_dotenv()
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

# 
# UNIVERSAL PROXY FIX: 
# This handles the headers from the KWS server automatically.
# It detects if the app is being accessed via /proxy/10000 or a direct subdomain.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# ==========================================
# 2. DATABASE POOLING LOGIC
# ==========================================
DATABASE_URL = os.environ.get("DATABASE_URL")
db_pool = None

def init_pool():
    global db_pool
    try:
        db_pool = psycopg2.pool.ThreadedConnectionPool(
            5, 50,
            dsn=DATABASE_URL,
            sslmode="disable",
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
# 3. UNIVERSAL ROUTES (Works for Home & College)
# ==========================================

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
    
    # 🔥 1. INITIALIZE DEFAULTS
    output = ""
    user_code = ""
    question = None
    test_results = []
    all_passed = False

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM questions WHERE id=%s", (qid,))
        question = cur.fetchone()
        test_cases = TEST_CASES_DICT.get(qid, [])

        if request.method == "POST":
            user_code = request.form["user_code"]
            language = request.form.get("lang_choice", "python")

            # 🔥 2. PROCESS SUBMISSION VIA QUEUE
            job_id = submit_job(user=session["user"], code=user_code, language=language, test_cases=test_cases)
            result = get_result(job_id)

            # Extract data from the result object
            test_results = result.get("test_results") or []
            all_passed = result.get("all_passed", False)
            total_cases = len(test_results)
            passed_cases = sum(1 for r in test_results if r.get("passed"))

            # Build the summary message for the terminal
            if all_passed:
                output = f"✅ SUCCESS: {passed_cases}/{total_cases} Test Cases Passed!"
            else:
                failed_test = next((r for r in test_results if not r.get("passed")), None)
                if failed_test:
                    output = f"❌ FAILED: {passed_cases}/{total_cases} Passed"
                else:
                    output = "❌ ERROR: Execution was terminated (Time/Memory Limit Exceeded)."

            # 🔥 3. SAVE TO DATABASE (Only on POST)
            # This ensures Leaderboard and Admin Panel get updated immediately
            try:
                final_status = 'Success' if all_passed else 'Failed'
                
                # Record in submissions table (for Leaderboard)
                cur.execute("""
                    INSERT INTO submissions (username, problem_id, status, language)
                    VALUES (%s, %s, %s, %s)
                """, (session["user"], qid, final_status, language))
                
                # Record in attempts table (for Solutions & Deep Dive)
                # Using ON CONFLICT so one user doesn't create 1000 rows for the same problem
                cur.execute("""
                    INSERT INTO attempts (user_roll, question_id, status, code, language)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_roll, question_id, language) 
                    DO UPDATE SET code = EXCLUDED.code, status = EXCLUDED.status
                """, (session["user"], qid, final_status, user_code, language))
                
                conn.commit()
            except Exception as e:
                print(f"DATABASE SAVE ERROR: {e}")
                conn.rollback()
                    
    finally:
        # Crucial for handling 250 users: release connection back to pool
        release_db_connection(conn)

    # 🔥 4. RENDER TEMPLATE
    return render_template("question_detail.html", 
                           question=question, 
                           test_results=test_results, 
                           all_passed=all_passed,
                           user_code=user_code,
                           output=output)


# ==========================================
# 4. INSTRUCTIONS & RULES
# ==========================================

@app.route("/instructions")
def instructions():
    """
    Serves the 2x2 Quadrant Guide for all 4 languages.
    Ensures students know how to handle space-separated inputs.
    """
    if "user" not in session:
        return redirect(url_for("login"))
    
    # This renders the quadrant HTML we designed
    return render_template("instructions.html")

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
    if "user" not in session: 
        return redirect(url_for("login"))
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

@app.route("/admin")
def admin():
    # 1. Security Check
    if not session.get("is_admin"): 
        return redirect(url_for("home"))
    
    from datetime import datetime
    # IST is your defined timezone object
    today_str = datetime.now(IST).strftime('%Y-%m-%d')
    selected_date = request.args.get('date', today_str) 
    
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 2. Get the specific question for the selected date
        cur.execute("SELECT id, title, date FROM questions WHERE date = %s LIMIT 1", (selected_date,))
        q_info = cur.fetchone()
        
        # 3. Attendance Query
        # We look for a 'Success' status for the specific problem_id linked to that date
        query = """
            SELECT 
                u.roll_no, 
                u.name,
                CASE 
                    WHEN s.status = 'Success' THEN 'Completed'
                    ELSE 'Pending'
                END as status,
                s.created_at as timestamp
            FROM users u
            LEFT JOIN (
                SELECT DISTINCT ON (username) username, status, created_at
                FROM submissions
                WHERE problem_id = %s AND status = 'Success'
                ORDER BY username, created_at ASC
            ) s ON u.roll_no = s.username
            WHERE u.flag = 0 
            ORDER BY u.roll_no ASC
        """
        # If no question exists for that date, problem_id is set to 0
        cur.execute(query, (q_info['id'] if q_info else 0,))
        report = cur.fetchall()
        
    finally: 
        release_db_connection(conn)

    return render_template("admin.html", report=report, q_info=q_info, selected_date=selected_date)



@app.route("/admin/track/<roll_no>")
def admin_track(roll_no):
    if not session.get("is_admin"):
        return redirect(url_for("home"))
    
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Count DISTINCT solved problems for the Leaderboard/Total
        cur.execute("SELECT DISTINCT problem_id FROM submissions WHERE username=%s AND status='Success'", (roll_no,))
        solved_ids = [r['problem_id'] for r in cur.fetchall()]
        
        # 2. Heatmap Data: Count how many unique problems solved per day
        heatmap_query = """
            SELECT TO_CHAR(created_at, 'YYYY-MM-DD') as sub_date, 
                   COUNT(DISTINCT problem_id) as daily_count
            FROM submissions 
            WHERE username = %s AND status = 'Success'
            GROUP BY sub_date
        """
        cur.execute(heatmap_query, (roll_no,))
        # Convert to dictionary for the frontend: {'2026-02-01': 5, '2026-02-02': 2}
        heatmap = {r['sub_date']: r['daily_count'] for r in cur.fetchall()}
        
    finally:
        release_db_connection(conn)
        
    return render_template("admin_use_detail.html", user=roll_no, solved=solved_ids, heatmap=heatmap)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    # 🔥 IMPORTANT FOR PUBLISHING: bind to 0.0.0.0
    app.run(host="0.0.0.0", port=10000, debug=False)