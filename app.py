import os
import io
import json
import subprocess
import multiprocessing
import psycopg2
import psycopg2.extras
import pytz
import tempfile
import builtins
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from contextlib import redirect_stdout
from dotenv import load_dotenv
from psycopg2 import pool

load_dotenv()
IST = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

# ==========================================
# 1. RESILIENT DATABASE POOLING
# ==========================================
DATABASE_URL = os.environ.get("DATABASE_URL")

db_config = {
    "dsn": DATABASE_URL,
    "sslmode": "require",
    "connect_args": {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    }
}

try:
    # Threaded pool handles concurrent requests from 500 students better than SimplePool
    db_pool = psycopg2.pool.ThreadedConnectionPool(5, 50, **db_config)
    print("Database connection pool established with TCP Keepalives.")
except Exception as e:
    print(f"Critical Pool Error: {e}")

def get_db_connection():
    conn = db_pool.getconn()
    try:
        with conn.cursor() as cur:
            cur.execute('SELECT 1')
    except (psycopg2.OperationalError, psycopg2.InterfaceError):
        db_pool.putconn(conn, close=True)
        conn = db_pool.getconn()
    return conn

def release_db_connection(conn):
    db_pool.putconn(conn)

# ==========================================
# 2. OPTIMIZED EXECUTION ENGINE
# ==========================================
def execute_user_code(user_code, test_cases, queue, lang='python'):
    passed_cases = 0
    results_summary = []
    total_cases = len(test_cases)
    safe_builtins = {k: getattr(builtins, k) for k in dir(builtins)}

    if lang == 'java':
        with tempfile.TemporaryDirectory() as tmp_dir:
            java_file = os.path.join(tmp_dir, "Solution.java")
            clean_code = "\n".join([line for line in user_code.splitlines() if not line.strip().startswith("package ")])
            with open(java_file, "w") as jf:
                jf.write(clean_code)
            
            cp = subprocess.run(['javac', java_file], capture_output=True, text=True, timeout=10)
            if cp.returncode != 0:
                queue.put({'all_passed': False, 'summary': "0/0", 'details': cp.stderr})
                return

            for case in test_cases:
                try:
                    rp = subprocess.run(['java', '-cp', tmp_dir, '-Xmx128m', 'Solution', case['input_data']], 
                                        capture_output=True, text=True, timeout=5)
                    actual = rp.stdout.strip().lower()
                    expected = str(case['expected_output']).strip().lower()
                    passed = (actual == expected)
                    if passed: passed_cases += 1
                    results_summary.append({'input': case['input_data'], 'passed': passed, 'actual': actual, 'expected': expected})
                except Exception as e:
                    results_summary.append({'input': case['input_data'], 'passed': False, 'actual': str(e)})

    elif lang == 'python':
        for case in test_cases:
            f = io.StringIO()
            try:
                exec_scope = {"input_val": json.loads(case['input_data']), "output_val": None, "__builtins__": safe_builtins}
                with redirect_stdout(f):
                    exec(user_code, exec_scope)
                res = str(exec_scope.get("output_val")).strip().lower() if exec_scope.get("output_val") is not None else f.getvalue().strip().lower()
                expected = str(case['expected_output']).strip().lower()
                passed = (res == expected)
                if passed: passed_cases += 1
                results_summary.append({'input': case['input_data'], 'passed': passed, 'actual': res, 'expected': expected})
            except Exception as e:
                results_summary.append({'input': case['input_data'], 'passed': False, 'actual': f"Error: {str(e)}"})

    queue.put({'all_passed': passed_cases == total_cases, 'summary': f"{passed_cases}/{total_cases}", 'details': results_summary})

# ==========================================
# 3. ROUTES (AUTH, CONTENT, SOLUTIONS)
# ==========================================

@app.route("/")
def index():
    return redirect(url_for("home")) if "user" in session else redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form["username"].upper(), request.form["password"]
        conn = get_db_connection()
        try:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM users WHERE roll_no=%s AND password=%s", (username, password))
            user = cur.fetchone()
            if user:
                session.update({"user": username, "is_admin": user.get('is_admin', False)})
                return redirect(url_for("home"))
        finally: release_db_connection(conn)
    return render_template("login.html")

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
    finally: release_db_connection(conn)
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
            LEFT JOIN attempts a ON s.username = a.user_roll 
                AND s.problem_id = a.question_id 
                AND s.language = a.language
            WHERE s.username = %s AND s.status = 'Success'
            ORDER BY s.created_at DESC
        """, (session["user"],))
        user_solutions = cur.fetchall()
    finally: release_db_connection(conn)
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
            u_code, lang = request.form["user_code"], request.form.get("lang_choice", "python") 
            queue = multiprocessing.Queue()
            p = multiprocessing.Process(target=execute_user_code, args=(u_code, t_cases, queue, lang))
            p.start(); p.join(timeout=25)

            if p.is_alive():
                p.terminate(); output = "❌ Timeout Error (25s exceeded)"
            elif not queue.empty():
                res = queue.get()
                if res.get('all_passed'):
                    output = f"✅ SUCCESS! {res['summary']} cases passed."
                    cur.execute("INSERT INTO submissions (username, problem_id, status, language) VALUES (%s, %s, 'Success', %s)", (session['user'], qid, lang))
                    cur.execute("INSERT INTO attempts (user_roll, question_id, status, code, language) VALUES (%s, %s, 'Completed', %s, %s) ON CONFLICT (user_roll, question_id, language) DO UPDATE SET status='Completed', code=EXCLUDED.code", (session['user'], qid, u_code, lang))
                    conn.commit()
                else:
                    failed = next((c for c in res['details'] if not c['passed']), res['details'][0])
                    output = f"❌ FAILED ({res['summary']})\nInput: {failed['input']}\nExpected: {failed['expected']}\nActual: {failed['actual']}"
    finally: release_db_connection(conn)
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
    finally: release_db_connection(conn)
    return render_template('leaderboard.html', rankings=rankings)

# ==========================================
# 4. ADMIN & TRACKING ROUTES
# ==========================================

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
    finally: release_db_connection(conn)
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
    finally: release_db_connection(conn)
    return render_template("admin_use_detail.html", user=user, solved=solved, heatmap=heatmap)

@app.route("/logout")
def logout():
    session.clear(); return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))