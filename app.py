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
import csv
from io import StringIO
from flask import Response, make_response

# ==========================================
# 1. INITIALIZATION & CONFIGURATION
# ==========================================
load_dotenv()
IST = pytz.timezone('Asia/Kolkata')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "local_development_only_key")

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
                
                # 🟢 ADD THIS LINE:
                session["flag1"] = int(user.get("flag1") or 0)
                session.permanent = True 
                session.modified = True
                return redirect(url_for("home"))
            else:
                # Optional: Add an error message if login fails
                return render_template("login.html", error="Invalid credentials")
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
    
    # INITIALIZE DEFAULTS
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
            # SECURITY & COMPATIBILITY: Handle both JSON and Form data
            if request.is_json:
                data = request.get_json()
                user_code = data.get("user_code", "")
                language = data.get("lang_choice", "python")
            else:
                user_code = request.form.get("user_code", "")
                language = request.form.get("lang_choice", "python")

            # PROCESS SUBMISSION VIA QUEUE
            job_id = submit_job(user=session["user"], code=user_code, language=language, test_cases=test_cases)
            result = get_result(job_id)

            # Extract data from the result object
            test_results = result.get("test_results") or []
            all_passed = result.get("all_passed", False)
            passed_cases = sum(1 for r in test_results if r.get("passed"))
            total_cases = len(test_results)
            
            # 🔎 1. SYNTAX ERROR DETECTION LOGIC 🔍
            # We check the first failed test case to see if it crashed during compilation/startup
            first_fail = next((r for r in test_results if not r.get("passed")), None)
            is_syntax_error = False
            error_msg = ""
            line_no = None

            if first_fail and first_fail.get("exit_code") != 0:
                raw_error = first_fail.get("error", "")
                if raw_error:
                    # 🛡️ CLEANING LOGIC: Remove NsJail internal logs and messy paths
                    lines = raw_error.split('\n')
                    # Filter out lines starting with [I] (NsJail info) or [W] (Warnings)
                    filtered_lines = [line for line in lines if not line.startswith(('[I]', '[W]', '[E]'))]
                    
                    # Reconstruct the message
                    clean_msg = "\n".join(filtered_lines).strip()
                    
                    # Optional: Remove the long server path to make it look cleaner
                    # This replaces '/home/thala_thalapathy/.../s.py' with just 'script.py'
                    clean_msg = re.sub(r'/home/[\w\-/._]+/', '', clean_msg)
                    
                    is_syntax_error = True
                    error_msg = clean_msg

                    # 🔍 REGEX: Find line number for Monaco highlight
                    line_match = re.search(r'(?:line\s+|:)(\d+)', error_msg, re.IGNORECASE)
                    if line_match:
                        line_no = int(line_match.group(1))



            # Build summary message for terminal/modals
            if all_passed:
                output = f"✅ SUCCESS: {passed_cases}/{total_cases} Test Cases Passed!"
            elif is_syntax_error:
                output = "❌ ERROR: Compilation/Syntax Failure"
            else:
                output = f"❌ FAILED: {passed_cases}/{total_cases} Passed"

            # DATABASE SAVE
            try:
                final_status = 'Success' if all_passed else 'Failed'
    
            # 1. We ALWAYS log the submission history (to see their path)
                cur.execute("""
                INSERT INTO submissions (username, problem_id, status, language)
                VALUES (%s, %s, %s, %s)
                """, (session["user"], qid, final_status, language))
    
            # 2. We ONLY update the 'attempts' (Solutions) table if they actually PASSED
            # Or, if it's their very first attempt, we save it regardless.
                if all_passed:
                    cur.execute("""
                    INSERT INTO attempts (user_roll, question_id, status, code, language)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_roll, question_id, language) 
                    DO UPDATE SET 
                    code = EXCLUDED.code, 
                    status = EXCLUDED.status
                    """, (session["user"], qid, final_status, user_code, language))
    
                conn.commit()
            except Exception as e:
                print(f"DATABASE SAVE ERROR: {e}")
                conn.rollback()

            # AJAX RESPONSE: Send JSON to trigger the Monaco Popups
            if request.is_json:
                return jsonify({
                    "status": "success" if all_passed else "error",
                    "is_syntax_error": is_syntax_error, # 🟢 Tell UI to show Bright Red Popup
                    "passed_all": all_passed,
                    "error_type": "Syntax Error" if is_syntax_error else "Logic Error",
                    "message": error_msg if is_syntax_error else "One or more test cases failed.",
                    "line": line_no, # 🟢 Monaco will highlight this line
                    "test_results": test_results,
                    "terminal_output": output
                })
                    
    finally:
        release_db_connection(conn)

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
        
        def get_top_5(flag1_val=None):
            # Base Query focusing on top 5 per category
            query = """
                SELECT u.roll_no, u.name, u.section, COUNT(DISTINCT s.problem_id) total
                FROM users u
                LEFT JOIN submissions s ON u.roll_no = s.username AND s.status='Success'
                WHERE u.flag = 0
            """
            params = []
            if flag1_val is not None:
                query += " AND u.flag1 = %s"
                params.append(flag1_val)
                
            query += " GROUP BY u.roll_no, u.name, u.section ORDER BY total DESC, u.roll_no ASC LIMIT 5"
            cur.execute(query, params)
            return cur.fetchall()

        # Fetch the 4 specific lists
        overall = get_top_5()       # Whole College Top 5
        sec_c = get_top_5(0)        # Section C Top 5 (flag1 = 0)
        sec_b = get_top_5(2)        # Section B Top 5 (flag1 = 1)
        sec_a = get_top_5(3)        # Section A Top 5 (flag1 = 3)

    finally:
        release_db_connection(conn)
        
    return render_template("leaderboard.html", 
                           overall=overall, 
                           sec_a=sec_a, 
                           sec_b=sec_b, 
                           sec_c=sec_c)

@app.route("/solutions")
def solutions():
    if "user" not in session: 
        return redirect(url_for("login"))
        
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 🟢 FIX: Only get the LATEST successful code for each problem/language combo
        cur.execute("""
            SELECT DISTINCT ON (s.problem_id, s.language)
                s.status, 
                s.created_at, 
                s.language, 
                q.title,
                q.date, 
                a.code
            FROM submissions s 
            JOIN questions q ON s.problem_id = q.id 
            LEFT JOIN attempts a ON s.username = a.user_roll 
                AND s.problem_id = a.question_id 
                AND s.language = a.language
            WHERE s.username = %s AND s.status = 'Success'
            ORDER BY s.problem_id, s.language, s.created_at DESC
        """, (session["user"],))
        
        user_solutions = cur.fetchall()
    finally: 
        release_db_connection(conn)
        
    return render_template("solutions.html", solutions=user_solutions)
@app.route("/admin")
def admin():
    if not session.get("is_admin"): 
        return redirect(url_for("home"))
    
    admin_id = session.get("user")
    # Set the minimum date to December 24, 2025
    MIN_DATE = "2025-12-24"
    from datetime import datetime
    today_str = datetime.now(IST).strftime('%Y-%m-%d')
    selected_date = request.args.get('date', today_str) 
    
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Fetching the specific question including its assigned date
        cur.execute("SELECT id, title, date FROM questions WHERE date = %s LIMIT 1", (selected_date,))
        q_info = cur.fetchone()
        
        # Mapping for Section Filters based on staff ID
        view_map = {'24CP001': 0, '24CP002': 2, '24CP003': 3, '24JTA01': 3, '24JTB01': 2, '24JTC01': 0}
        
        if admin_id in ['24UCS027', 'HODCSE01']:
            filter_condition = "u.flag = 0"
            params = (q_info['id'] if q_info else 0,)
            display_name = "All Sections"
        else:
            target_flag1 = view_map.get(admin_id, 0)
            filter_condition = "u.flag = 0 AND u.flag1 = %s"
            params = (q_info['id'] if q_info else 0, target_flag1)
            display_name = {0: 'CSE-C', 2: 'CSE-B', 3: 'CSE-A'}.get(target_flag1, "Unknown")

        # Query updated to prioritize Java Count and display the latest daily status
        query = f"""
            SELECT 
                u.roll_no, u.name, u.section,
                CASE WHEN s_today.status = 'Success' THEN 'Completed' ELSE 'Pending' END as status,
                s_today.created_at as timestamp,
                COALESCE(stats.java_solved, 0) as java_count
            FROM users u
            LEFT JOIN (
                SELECT DISTINCT ON (username) username, status, created_at
                FROM submissions
                WHERE problem_id = %s AND status = 'Success'
                ORDER BY username, created_at ASC
            ) s_today ON u.roll_no = s_today.username
            LEFT JOIN (
                SELECT username,
                    COUNT(DISTINCT CASE WHEN language = 'java' THEN problem_id END) as java_solved
                FROM submissions WHERE status = 'Success'
                GROUP BY username
            ) stats ON u.roll_no = stats.username
            WHERE {filter_condition}
            ORDER BY u.roll_no ASC
        """
        cur.execute(query, params)
        report = cur.fetchall()
        
    finally: 
        release_db_connection(conn)

    return render_template("admin.html", 
                           report=report, 
                           q_info=q_info, 
                           selected_date=selected_date, 
                           min_date=MIN_DATE,
                           count=len(report),
                           section_name=display_name)


@app.route("/admin/export")
def export_report():
    if not session.get("is_admin"):
        return redirect(url_for("home"))

    admin_id = session.get("user")
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Determine filter (Same logic as your admin route)
        if admin_id in ['24UCS027', 'HODCSE01']:
            filter_condition = "u.flag = 0"
            params = []
        else:
            view_map = {'24CP001': 0, '24CP002': 2, '24CP003': 3, '24JTA01': 3, '24JTB01': 2, '24JTC01': 0}
            target_flag1 = view_map.get(admin_id, 0)
            filter_condition = "u.flag = 0 AND u.flag1 = %s"
            params = [target_flag1]

        # Fetch Data
        query = f"""
            SELECT 
                u.roll_no, u.name, u.section,
                COALESCE(stats.total_solved, 0) as total,
                COALESCE(stats.java_solved, 0) as java,
                COALESCE(stats.py_solved, 0) as python,
                COALESCE(stats.cpp_solved, 0) as cpp
            FROM users u
            LEFT JOIN (
                SELECT username,
                    COUNT(DISTINCT problem_id) as total_solved,
                    COUNT(DISTINCT CASE WHEN language = 'java' THEN problem_id END) as java_solved,
                    COUNT(DISTINCT CASE WHEN language = 'python' THEN problem_id END) as py_solved,
                    COUNT(DISTINCT CASE WHEN language = 'cpp' THEN problem_id END) as cpp_solved
                FROM submissions WHERE status = 'Success'
                GROUP BY username
            ) stats ON u.roll_no = stats.username
            WHERE {filter_condition} ORDER BY u.roll_no ASC
        """
        cur.execute(query, params)
        rows = cur.fetchall()

        # Generate CSV
        si = StringIO()
        cw = csv.writer(si)
        cw.writerow(['Roll No', 'Name', 'Section', 'Total Solved', 'Java', 'Python', 'C++'])
        for r in rows:
            cw.writerow([r['roll_no'], r['name'], r['section'], r['total'], r['java'], r['python'], r['cpp']])
        
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = f"attachment; filename=Progress_Report_{admin_id}.csv"
        output.headers["Content-type"] = "text/csv"
        return output
    finally:
        release_db_connection(conn)



@app.route("/admin/track/<roll_no>")
def admin_track(roll_no):
    if not session.get("is_admin"):
        return redirect(url_for("home"))
    
    conn = get_db_connection()
    solved_data = [] 
    heatmap = {}
    lang_counts = {'python': 0, 'cpp': 0, 'java': 0, 'javascript': 0}
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 🟢 1. FETCH UNIQUE PROBLEM+LANGUAGE PAIRS
        # This prevents duplicate counts if they submit "Palindrome" in Java twice.
        cur.execute("""
            SELECT DISTINCT ON (s.problem_id, s.language) 
                q.title, s.language, s.created_at, s.problem_id
            FROM submissions s
            JOIN questions q ON s.problem_id = q.id
            WHERE s.username = %s AND s.status = 'Success'
            ORDER BY s.problem_id, s.language, s.created_at DESC
        """, (roll_no,))
        solved_data = cur.fetchall() 

        # 🟢 2. CALCULATE ACCURATE LANGUAGE COUNTS
        for item in solved_data:
            lang = item['language'].lower()
            if lang in lang_counts:
                lang_counts[lang] += 1

        # 🟢 3. HEATMAP STREAK (COUNT UNIQUE PROBLEMS PER DAY)
        heatmap_query = """
            SELECT TO_CHAR(created_at, 'YYYY-MM-DD') as sub_date, 
                   COUNT(DISTINCT problem_id) as daily_count
            FROM submissions 
            WHERE username = %s AND status = 'Success'
            GROUP BY sub_date
        """
        cur.execute(heatmap_query, (roll_no,))
        heatmap = {r['sub_date']: r['daily_count'] for r in cur.fetchall()}
        
        # 🟢 4. TOTAL UNIQUE PROBLEM COUNT (The 1/90 stat)
        cur.execute("""
            SELECT COUNT(DISTINCT problem_id) as total 
            FROM submissions WHERE username = %s AND status = 'Success'
        """, (roll_no,))
        unique_problem_count = cur.fetchone()['total']
        
    finally:
        release_db_connection(conn)
        
    return render_template("admin_use_detail.html", 
                           user=roll_no, 
                           solved=solved_data, 
                           heatmap=heatmap, 
                           unique_count=unique_problem_count,
                           langs=lang_counts)
@app.route("/my-stats")
def my_stats():
    # 1. SECURITY: Ensure user is logged in
    if "user" not in session:
        return redirect(url_for("login"))
    if session.get("is_admin") == True and session.get("flag1") == 1:
        # Staff shouldn't be here, send them to the admin dashboard
        return redirect(url_for("admin"))
    
    roll_no = session["user"] # Get logged-in student's ID
    
    conn = get_db_connection()
    solved_data = [] 
    heatmap = {}
    lang_counts = {'python': 0, 'cpp': 0, 'java': 0, 'javascript': 0}
    
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 🟢 1. FETCH UNIQUE PROBLEM+LANGUAGE PAIRS
        # Ensures that if they solve "Palindrome" in Java and Python, it counts as 1 for each language.
        cur.execute("""
            SELECT DISTINCT ON (s.problem_id, s.language) 
                q.title, s.language, s.created_at, s.problem_id
            FROM submissions s
            JOIN questions q ON s.problem_id = q.id
            WHERE s.username = %s AND s.status = 'Success'
            ORDER BY s.problem_id, s.language, s.created_at DESC
        """, (roll_no,))
        solved_data = cur.fetchall() 

        # 🟢 2. CALCULATE ACCURATE LANGUAGE COUNTS
        for item in solved_data:
            lang = item['language'].lower()
            if lang in lang_counts:
                lang_counts[lang] += 1

        # 🟢 3. HEATMAP STREAK (COUNT UNIQUE PROBLEMS PER DAY)
        heatmap_query = """
            SELECT TO_CHAR(created_at, 'YYYY-MM-DD') as sub_date, 
                   COUNT(DISTINCT problem_id) as daily_count
            FROM submissions 
            WHERE username = %s AND status = 'Success'
            GROUP BY sub_date
        """
        cur.execute(heatmap_query, (roll_no,))
        heatmap = {r['sub_date']: r['daily_count'] for r in cur.fetchall()}
        
        # 🟢 4. TOTAL UNIQUE PROBLEM COUNT (The 1/90 stat)
        cur.execute("""
            SELECT COUNT(DISTINCT problem_id) as total 
            FROM submissions WHERE username = %s AND status = 'Success'
        """, (roll_no,))
        unique_problem_count = cur.fetchone()['total']
        
    finally:
        release_db_connection(conn)
        
    # Render the new student-specific template
    return render_template("my_stats.html", 
                            user=roll_no, 
                            solved=solved_data, 
                            heatmap=heatmap, 
                            unique_count=unique_problem_count,
                            langs=lang_counts)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    # 🔥 IMPORTANT FOR PUBLISHING: bind to 0.0.0.0
    app.run(host="0.0.0.0", port=10000, debug=False)
