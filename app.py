import os
import io
import json
import subprocess
import multiprocessing
import psycopg2
import psycopg2.extras
import pytz
import tempfile  # For thread-safe Java files
import shutil    # For cleanup
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from contextlib import redirect_stdout
from dotenv import load_dotenv
from datetime import datetime
from psycopg2 import pool # Essential for college server stability

load_dotenv()
IST = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

# Database Connection Pool
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create a pool: min 1 connection, max 20 (adjust based on server RAM)
try:
    db_pool = psycopg2.pool.SimpleConnectionPool(1, 20, DATABASE_URL, sslmode="require")
    print("Database connection pool created successfully")
except Exception as e:
    print(f"Error creating connection pool: {e}")

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)
def execute_user_code(user_code, test_cases, queue, lang='python'):
    total_cases = len(test_cases)
    passed_cases = 0
    results_summary = []

    for case in test_cases:
        expected_output = str(case['expected_output']).strip().lower()
        raw_input = case['input_data']
        case_result = {'input': raw_input, 'expected': expected_output, 'actual': '', 'passed': False, 'error': None}
        
        if lang == 'python':
            f = io.StringIO()
            try:
                # Use your existing JSON logic
                try:
                    processed_input = json.loads(raw_input)
                except:
                    processed_input = raw_input 

                # SECURITY: Remove sensitive builtins for college server
                safe_builtins = __builtins__.copy()
                # Optional: del safe_builtins['open'], safe_builtins['__import__']
                
                exec_scope = {"input_val": processed_input, "output_val": None, "__builtins__": safe_builtins}
                with redirect_stdout(f):
                    exec(user_code, exec_scope)
                
                variable_output = str(exec_scope.get("output_val")).strip().lower() if exec_scope.get("output_val") is not None else ""
                printed_output = f.getvalue().strip().lower()
                actual_output = variable_output if variable_output else printed_output
                case_result['actual'] = actual_output
                case_result['passed'] = (actual_output == expected_output)
            except Exception as e:
                case_result['error'] = f"Python Error: {str(e)}"
                case_result['actual'] = f"Error: {str(e)}"
                
        elif lang == 'java':
            # FIX: Use temporary directory to prevent file overwrite
            with tempfile.TemporaryDirectory() as tmp_dir:
                java_file = os.path.join(tmp_dir, "Solution.java")
                clean_input = raw_input.replace('[', '').replace(']', '')
                
                lines = user_code.splitlines()
                user_code_clean = "\n".join([line for line in lines if not line.strip().startswith("package ")])

                try:
                    with open(java_file, "w") as jf:
                        jf.write(user_code_clean)
                    
                    # Compile in tmp_dir
                    cp = subprocess.run(['javac', java_file], capture_output=True, text=True, timeout=10)
                    if cp.returncode != 0:
                        case_result['error'] = "Compilation Error"
                        case_result['actual'] = cp.stderr
                    else:
                        # Run from tmp_dir
                        rp = subprocess.run(['java', '-cp', tmp_dir, '-Xmx128m', 'Solution', clean_input], capture_output=True, text=True, timeout=5)
                        actual_output = rp.stdout.strip().lower()
                        case_result['actual'] = actual_output
                        case_result['passed'] = (actual_output == expected_output)
                except Exception as e:
                    case_result['error'] = f"Java Runtime Error: {str(e)}"

        if case_result['passed']: passed_cases += 1
        results_summary.append(case_result)

    queue.put({'all_passed': passed_cases == total_cases, 'summary': f"{passed_cases}/{total_cases}", 'details': results_summary})
# --- Authentication Routes ---

@app.route("/")
def index():
    if "user" in session: return redirect(url_for("home"))
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
            cur.close()
            if user:
                session["user"] = username
                session["is_admin"] = user.get('is_admin', False)
                return redirect(url_for("home"))
        finally:
            release_db_connection(conn) #
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Content Routes ---

@app.route("/home")
def home():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])

@app.route("/questions")
def questions():
    if "user" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM questions ORDER BY id ASC")
        qs = cur.fetchall()
        cur.close()
    finally:
        release_db_connection(conn)
    return render_template("questions.html", questions=qs)

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
            LEFT JOIN attempts a ON s.username = a.user_roll AND s.problem_id = a.question_id AND s.language = a.language
            WHERE s.username = %s ORDER BY s.created_at DESC
        """, (session["user"],))
        user_solutions = cur.fetchall()
        cur.close()
    finally:
        release_db_connection(conn)
    return render_template("solutions.html", solutions=user_solutions)

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question_detail(qid):
    if "user" not in session: return redirect(url_for("login"))
    output, u_code = "", ""
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM questions WHERE id=%s", (qid,))
        q = cur.fetchone()
        cur.execute("SELECT input_data, expected_output FROM test_cases WHERE question_id=%s", (qid,))
        t_cases = cur.fetchall()

        if request.method == "POST":
            u_code = request.form["user_code"]
            lang = request.form.get("lang_choice", "python") 
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=execute_user_code, args=(u_code, t_cases, queue, lang))
            p.start(); p.join(timeout=25)

            if p.is_alive():
                p.terminate(); output = "❌ Timeout Error"
            elif not queue.empty():
                res = queue.get()
                if res.get('all_passed'):
                    output = f"✅ SUCCESS! {res['summary']} cases passed."
                    cur.execute("""
                        INSERT INTO attempts (user_roll, question_id, status, code)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (user_roll, question_id)
                        DO UPDATE SET status='Completed', code=EXCLUDED.code, timestamp=CURRENT_TIMESTAMP
                    """, (session["user"], qid, "Completed", u_code))
                    cur.execute("INSERT INTO submissions (username, problem_id, status) VALUES (%s, %s, %s)", (session['user'], qid, 'Success'))
                    conn.commit()
                else:
                    failed = next((c for c in res['details'] if not c['passed']), None)
                    output = f"❌ FAILED ({res['summary']})\nInput: {failed['input']}\nExpected: {failed['expected']}\nActual: {failed['actual']}"
        cur.close()
    finally:
        release_db_connection(conn)
    return render_template("question_detail.html", question=q, output=output, user_code=u_code)

@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT username, COUNT(DISTINCT problem_id) as total, 
                   MAX(created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as last_solve
            FROM submissions WHERE status = 'Success'
            GROUP BY username ORDER BY total DESC, last_solve ASC LIMIT 50
        """)
        rankings = cur.fetchall() 
        cur.close()
    finally:
        release_db_connection(conn)
    return render_template('leaderboard.html', rankings=rankings)

# --- Admin Routes ---

@app.route("/admin")
@app.route("/admin/<int:qid>")
def admin(qid=1):
    if not session.get("is_admin"): return redirect(url_for("home"))
    selected_date = request.args.get('date')
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        if selected_date:
            cur.execute("SELECT id FROM questions WHERE date = %s", (selected_date,))
            q_res = cur.fetchone()
            if q_res: qid = q_res['id']

        cur.execute("SELECT id, title, date FROM questions WHERE id = %s", (qid,))
        q_info = cur.fetchone()
        cur.execute("""
            SELECT u.roll_no, u.name, COALESCE(a.status, 'Pending') as status,
                   a.timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata' as timestamp
            FROM users u LEFT JOIN attempts a ON u.roll_no = a.user_roll AND a.question_id = %s
            ORDER BY status ASC, u.roll_no ASC
        """, (qid,))
        report = cur.fetchall()
        cur.close()
    finally:
        release_db_connection(conn)
    return render_template("admin.html", report=report, q_info=q_info, qid=qid, selected_date=selected_date)

@app.route("/admin/track/<user>")
def admin_track(user):
    if not session.get("is_admin"): return redirect(url_for("home"))
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT problem_id FROM submissions WHERE username = %s AND status = 'Success'", (user,))
        solved = [row['problem_id'] for row in cur.fetchall()]
        cur.execute("""
            SELECT DATE(created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as date, COUNT(*) as count
            FROM submissions WHERE username = %s AND status = 'Success' GROUP BY date
        """, (user,))
        heatmap = {str(row['date']): row['count'] for row in cur.fetchall()}
        cur.close()
    finally:
        release_db_connection(conn)
    return render_template("admin_use_detail.html", user=user, solved=solved, heatmap=heatmap)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    try:
        # host="0.0.0.0" is required for both Render and College Cloud
        app.run(host="0.0.0.0", port=port)
    finally:
        # This ensures the 500-student connection pool closes cleanly
        if 'db_pool' in globals():
            db_pool.closeall()
            print("Database pool closed.")
            