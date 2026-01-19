import os
import io
import json
import subprocess
import multiprocessing
import psycopg2
import psycopg2.extras
import pytz
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from contextlib import redirect_stdout
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

IST = pytz.timezone('Asia/Kolkata')
app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

# Database Connection
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

import json
import io
import os
import subprocess
from contextlib import redirect_stdout

def execute_user_code(user_code, test_cases, queue, lang='python'):
    total_cases = len(test_cases)
    passed_cases = 0
    results_summary = []

    for case in test_cases:
        # Standardize expected output to lowercase string for comparison
        expected_output = str(case['expected_output']).strip().lower()
        raw_input = case['input_data']
        
        case_result = {'input': raw_input, 'expected': expected_output, 'actual': '', 'passed': False, 'error': None}
        
        if lang == 'python':
            f = io.StringIO()
            try:
                # --- PYTHON DATA CONVERSION ---
                # Converts "[3, 5, 1, 9]" string into a real Python list
                try:
                    processed_input = json.loads(raw_input)
                except:
                    processed_input = raw_input # Fallback if it's just a plain string

                # Inject input_val as a real object (List, Int, or String)
                exec_scope = {"input_val": processed_input, "output_val": None, "__builtins__": __builtins__}
                
                with redirect_stdout(f):
                    exec(user_code, exec_scope)
                
                # Priority 1: output_val variable | Priority 2: print() output
                variable_output = str(exec_scope.get("output_val")).strip().lower() if exec_scope.get("output_val") is not None else ""
                printed_output = f.getvalue().strip().lower()
                
                actual_output = variable_output if variable_output else printed_output
                case_result['actual'] = actual_output
                case_result['passed'] = (actual_output == expected_output)
            except Exception as e:
                case_result['error'] = f"Python Error: {str(e)}"
                case_result['actual'] = f"Error: {str(e)}"
                
        elif lang == 'java':
            # --- JAVA DATA CLEANING ---
            # Remove [ ] so student gets "3, 5, 1, 9" instead of "[3, 5, 1, 9]"
            clean_input = raw_input.replace('[', '').replace(']', '')

            # Automatically strip package statements
            lines = user_code.splitlines()
            user_code = "\n".join([line for line in lines if not line.strip().startswith("package ")])

            java_file = "Solution.java"
            class_file = "Solution.class"
            try:
                with open(java_file, "w") as f:
                    f.write(user_code)
                
                # Compile Java code
                compile_process = subprocess.run(['javac', java_file], capture_output=True, text=True, timeout=10)
                if compile_process.returncode != 0:
                    case_result['error'] = "Compilation Error"
                    case_result['actual'] = compile_process.stderr
                else:
                    # Pass the clean_input to args[0]
                    run_process = subprocess.run(['java', '-Xmx128m', 'Solution', clean_input], capture_output=True, text=True, timeout=5)
                    actual_output = run_process.stdout.strip().lower()
                    case_result['actual'] = actual_output
                    case_result['passed'] = (actual_output == expected_output)
            except Exception as e:
                case_result['error'] = f"Java Runtime Error: {str(e)}"
            finally:
                # Cleanup temporary files
                for f_path in [java_file, class_file]:
                    if os.path.exists(f_path): os.remove(f_path)

        if case_result['passed']: passed_cases += 1
        results_summary.append(case_result)

    queue.put({
        'all_passed': passed_cases == total_cases, 
        'summary': f"{passed_cases}/{total_cases}", 
        'details': results_summary
    })

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
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM users WHERE roll_no=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close(); conn.close()
        if user:
            session["user"] = username
            session["is_admin"] = user.get('is_admin', False)
            return redirect(url_for("home"))
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
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM questions ORDER BY id ASC")
    qs = cur.fetchall()
    cur.close(); conn.close()
    return render_template("questions.html", questions=qs)

@app.route("/solutions")
def solutions():
    if "user" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # We join submissions (for status), questions (for title/date), 
    # and attempts (for the actual code written)
    cur.execute("""
    SELECT 
        s.status, 
        s.created_at, 
        s.language,
        q.title, 
        q.date, 
        a.code
    FROM submissions s 
    JOIN questions q ON s.problem_id = q.id 
    LEFT JOIN attempts a ON 
        s.username = a.user_roll AND 
        s.problem_id = a.question_id AND 
        s.language = a.language
    WHERE s.username = %s 
    ORDER BY s.created_at DESC
""", (session["user"],))
    
    user_solutions = cur.fetchall()
    cur.close(); conn.close()
    return render_template("solutions.html", solutions=user_solutions)



@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question_detail(qid):
    if "user" not in session: return redirect(url_for("login"))
    output = ""
    u_code = ""
    conn = get_db_connection()
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
            p.terminate()
            output = "❌ Timeout Error"
        elif not queue.empty():
            res = queue.get()
            if res.get('all_passed'):
                output = f"✅ SUCCESS! {res['summary']} cases passed."
                try:
                    cur.execute("""
                        INSERT INTO attempts (user_roll, question_id, status, code)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (user_roll, question_id)
                        DO UPDATE SET status='Completed', code=EXCLUDED.code, timestamp=CURRENT_TIMESTAMP
                    """, (session["user"], qid, "Completed", u_code))
                    
                    cur.execute("INSERT INTO submissions (username, problem_id, status) VALUES (%s, %s, %s)",
                                (session['user'], qid, 'Success'))
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    output = f"⚠️ DB Error: {str(e)}"
            else:
                failed = next((c for c in res['details'] if not c['passed']), None)
                output = f"❌ FAILED ({res['summary']})\nInput: {failed['input']}\nExpected: {failed['expected']}\nActual: {failed['actual']}"
    
    cur.close(); conn.close()
    return render_template("question_detail.html", question=q, output=output, user_code=u_code)

@app.route("/leaderboard")
def leaderboard():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT username, COUNT(DISTINCT problem_id) as total, 
               MAX(created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as last_solve
        FROM submissions 
        WHERE status = 'Success'
        GROUP BY username 
        ORDER BY total DESC, last_solve ASC 
        LIMIT 50
    """)
    rankings = cur.fetchall() 
    cur.close(); conn.close()
    return render_template('leaderboard.html', rankings=rankings)

# --- Admin Routes ---

@app.route("/admin")
@app.route("/admin/<int:qid>")
def admin(qid=1):
    if not session.get("is_admin"): 
        return redirect(url_for("home"))
    
    selected_date = request.args.get('date')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    if selected_date:
        cur.execute("SELECT id FROM questions WHERE date = %s", (selected_date,))
        q_result = cur.fetchone()
        if q_result: qid = q_result['id']

    cur.execute("SELECT id, title, date FROM questions WHERE id = %s", (qid,))
    q_info = cur.fetchone()

    cur.execute("""
        SELECT u.roll_no, u.name, 
               COALESCE(a.status, 'Pending') as status,
               a.timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata' as timestamp
        FROM users u
        LEFT JOIN attempts a ON u.roll_no = a.user_roll AND a.question_id = %s
        ORDER BY status ASC, u.roll_no ASC
    """, (qid,))
    report = cur.fetchall()
    
    cur.close(); conn.close()
    return render_template("admin.html", report=report, q_info=q_info, qid=qid, selected_date=selected_date)

@app.route("/admin/track/<user>")
def admin_track(user):
    if not session.get("is_admin"): return redirect(url_for("home"))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("SELECT problem_id FROM submissions WHERE username = %s AND status = 'Success'", (user,))
    solved = [row['problem_id'] for row in cur.fetchall()]
    
    cur.execute("""
        SELECT DATE(created_at AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as date, COUNT(*) as count
        FROM submissions WHERE username = %s AND status = 'Success' GROUP BY date
    """, (user,))
    heatmap = {str(row['date']): row['count'] for row in cur.fetchall()}
    
    cur.close(); conn.close()
    return render_template("admin_use_detail.html", user=user, solved=solved, heatmap=heatmap)

@app.route("/user/<roll_no>")
def user_profile(roll_no):
    if "user" not in session: return redirect(url_for("login"))
    return render_template("user.html", roll_no=roll_no)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)