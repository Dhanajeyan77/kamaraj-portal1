import re
import os
import json
import psycopg2
import psycopg2.extras
import pytz
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
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
    # SECURITY: Ensure user is logged in
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()
    
    # INITIALIZE DEFAULTS (Preserving your structure)
    output = ""
    user_code = ""
    question = None
    test_results = []
    all_passed = False

    try:
        # Fetch question details
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM questions WHERE id=%s", (qid,))
        question = cur.fetchone()
        test_cases = TEST_CASES_DICT.get(qid, [])

        if request.method == "POST":
            # SECURITY & COMPATIBILITY: Handle both JSON (Monaco) and Form data
            if request.is_json:
                data = request.get_json()
                user_code = data.get("user_code", "")
                language = data.get("lang_choice", "python")
            else:
                user_code = request.form.get("user_code", "")
                language = request.form.get("lang_choice", "python")

            # PROCESS SUBMISSION VIA QUEUE (Your original logic)
            job_id = submit_job(user=session["user"], code=user_code, language=language, test_cases=test_cases)
            result = get_result(job_id)

            # Extract data from the result object
            test_results = result.get("test_results") or []
            all_passed = result.get("all_passed", False)
            passed_cases = sum(1 for r in test_results if r.get("passed"))
            total_cases = len(test_results)

            # Build summary message for terminal/modals
            if all_passed:
                output = f"✅ SUCCESS: {passed_cases}/{total_cases} Test Cases Passed!"
            else:
                failed_test = next((r for r in test_results if not r.get("passed")), None)
                output = f"❌ FAILED: {passed_cases}/{total_cases} Passed" if failed_test else "❌ ERROR: Execution Terminated."

            # DATABASE SAVE (Critical for Leaderboard & Security)
            try:
                final_status = 'Success' if all_passed else 'Failed'
                
                # Record in submissions table (for Leaderboard)
                cur.execute("""
                    INSERT INTO submissions (username, problem_id, status, language)
                    VALUES (%s, %s, %s, %s)
                """, (session["user"], qid, final_status, language))
                
                # Record in attempts table (for Solutions)
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

            # AJAX RESPONSE: Send JSON to trigger the Monaco Popups
            if request.is_json:
                return jsonify({
                    "status": "success" if all_passed else "error",
                    "passed_all": all_passed,
                    "error_type": result.get("error_type", "Execution Error"),
                    "message": result.get("message", "Check test cases"),
                    "line": result.get("line"), # Line number for Monaco highlight
                    "test_results": test_results,
                    "terminal_output": output
                })
                    
    finally:
        # Crucial for 250 users: release connection back to pool
        release_db_connection(conn)

    # RENDER TEMPLATE (For initial GET request)
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
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # Added join to users table to get Section and Name
        cur.execute("""
            SELECT u.roll_no, u.name, u.section, COUNT(DISTINCT s.problem_id) total
            FROM users u
            LEFT JOIN submissions s ON u.roll_no = s.username AND s.status='Success'
            WHERE u.flag = 0
            GROUP BY u.roll_no, u.name, u.section 
            ORDER BY total DESC, u.roll_no ASC
            LIMIT 5
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
    
    admin_id = session.get("user")
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
        
        # --- DYNAMIC SECTION & FILTER LOGIC ---
        if admin_id == '24UCS027' or admin_id =='HODCSE01':
            filter_condition = "u.flag = 0"
            params = (q_info['id'] if q_info else 0,)
            display_name = "All Sections"
        else:
            # Chairperson view: Map ID to flag1
            # C=0, B=2, A=3
            view_map = {'24CP001': 0, '24CP002': 2, '24CP003': 3,'24JTA01':3,'24JTB01':2,'24JTC01':0}
            section_names = {0: 'CSE-C', 2: 'CSE-B', 3: 'CSE-A'}
            
            target_flag1 = view_map.get(admin_id, 0)
            filter_condition = "u.flag = 0 AND u.flag1 = %s"
            params = (q_info['id'] if q_info else 0, target_flag1)
            display_name = section_names.get(target_flag1, "Unknown Section")

        # 3. Attendance Query
        # We look for a 'Success' status for the specific problem_id linked to that date
        query = f"""
            SELECT 
                u.roll_no, 
                u.name,
                u.section,
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
            WHERE {filter_condition}
            ORDER BY u.roll_no ASC
        """
        
        cur.execute(query, params)
        report = cur.fetchall()
        student_count = len(report)
        
    finally: 
        release_db_connection(conn)

    return render_template("admin.html", 
                           report=report, 
                           q_info=q_info, 
                           selected_date=selected_date, 
                           count=student_count, 
                           section_name=display_name)


@app.route("/admin/track/<roll_no>")
def admin_track(roll_no):
    if not session.get("is_admin"):
        return redirect(url_for("home"))
    
    conn = get_db_connection()
    solved_data = [] 
    heatmap = {}
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Fetch solved problems JOINED with questions to get the title
        cur.execute("""
            SELECT DISTINCT ON (s.problem_id) 
                q.title, 
                s.language, 
                s.created_at 
            FROM submissions s
            JOIN questions q ON s.problem_id = q.id
            WHERE s.username = %s AND s.status = 'Success'
            ORDER BY s.problem_id, s.created_at DESC
        """, (roll_no,))
        solved_data = cur.fetchall() 
        
        # 2. Heatmap Data (Keep this as is)
        heatmap_query = """
            SELECT TO_CHAR(created_at, 'YYYY-MM-DD') as sub_date, 
                   COUNT(DISTINCT problem_id) as daily_count
            FROM submissions 
            WHERE username = %s AND status = 'Success'
            GROUP BY sub_date
        """
        cur.execute(heatmap_query, (roll_no,))
        heatmap = {r['sub_date']: r['daily_count'] for r in cur.fetchall()}
        
    finally:
        release_db_connection(conn)
        
    return render_template("admin_use_detail.html", user=roll_no, solved=solved_data, heatmap=heatmap)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    # 🔥 IMPORTANT FOR PUBLISHING: bind to 0.0.0.0
    app.run(host="0.0.0.0", port=10000, debug=False)