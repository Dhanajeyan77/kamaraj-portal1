from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import psycopg2.extras
import multiprocessing
import io
import os
import subprocess
from contextlib import redirect_stdout

app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"

# Fetch database URL from Render Environment Variables
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    # Use sslmode=require for Neon/PostgreSQL compatibility on Render
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn

def execute_user_code(user_code, expected_answer, queue, lang='python'):
    """
    Executes user code in a separate process and puts the result in a Queue.
    This avoids the socket/manager errors seen in Docker.
    """
    expected_output = str(expected_answer).strip().lower()
    result = {'output': '', 'is_correct': False, 'error': None}
    
    # --- PYTHON EXECUTION ---
    if lang == 'python':
        f = io.StringIO()
        try:
            local_vars = {}
            with redirect_stdout(f):
                # Execute Python code with restricted builtins
                exec(user_code, {"__builtins__": __builtins__}, local_vars)
            actual_output = f.getvalue().strip()
            result['output'] = actual_output
            result['is_correct'] = actual_output.lower() == expected_output
        except Exception as e:
            result['error'] = f"Python Error: {str(e)}"
            
    # --- JAVA EXECUTION ---
    elif lang == 'java':
        java_file = "Solution.java"
        class_file = "Solution.class"
        try:
            # 1. Write student code to file
            with open(java_file, "w") as f:
                f.write(user_code)
            
            # 2. Compile (Uses the JDK installed via Dockerfile)
            compile_process = subprocess.run(['javac', java_file], capture_output=True, text=True)
            
            if compile_process.returncode != 0:
                result['error'] = "Compilation Error:\n" + compile_process.stderr
            else:
                # 3. Execute
                run_process = subprocess.run(
                    ['java', 'Solution'], 
                    capture_output=True, 
                    text=True, 
                    timeout=15
                )
                actual_output = run_process.stdout.strip()
                result['output'] = actual_output
                result['is_correct'] = actual_output.lower() == expected_output
                
        except subprocess.TimeoutExpired:
            result['error'] = "Timeout Error: Your Java code took too long to run!"
        except Exception as e:
            result['error'] = f"Java Execution Error: {str(e)}"
        finally:
            # Cleanup temporary files
            for f_path in [java_file, class_file]:
                if os.path.exists(f_path):
                    os.remove(f_path)

    # Place the result in the shared Queue
    queue.put(result)

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
        selected_lang = request.form.get("lang_choice", "python") 
        
        # Use Queue for robust inter-process communication in Docker
        queue = multiprocessing.Queue()
        p = multiprocessing.Process(
            target=execute_user_code, 
            args=(user_code, q['expected_output'], queue, selected_lang)
        )
        p.start()
        p.join(timeout=5) # Join with a small buffer for Java compilation

        if p.is_alive():
            p.terminate()
            output = "❌ Timeout Error: Code took too long!"
        else:
            if not queue.empty():
                res = queue.get()
                if res.get('error'):
                    output = f"⚠️ {res['error']}"
                else:
                    actual = res.get('output', "")
                    if res.get('is_correct'):
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
            else:
                output = "⚠️ Error: Execution engine failed to return a result."
    
    cur.close()
    conn.close()
    return render_template("question_detail.html", question=q, output=output)

@app.route("/solutions")
def solutions():
    if "user" not in session:
        return redirect(url_for("login"))
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("""
        SELECT a.code, a.timestamp, q.date, q.content, q.title
        FROM attempts a
        JOIN questions q ON a.question_id = q.id
        WHERE a.user_roll = %s
    """, (session["user"],))
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
    cur.execute("SELECT is_admin FROM users WHERE roll_no=%s", (session["user"],))
    user = cur.fetchone()
    if not user or user['is_admin'] is not True:
        cur.close(); conn.close()
        return "Access Denied", 403
    cur.execute("SELECT date, title, content FROM questions WHERE id=%s", (qid,))
    q_info = cur.fetchone()
    cur.execute("""
        SELECT u.roll_no, u.name, a.status, 
               (a.timestamp AT TIME ZONE 'UTC' AT TIME ZONE 'Asia/Kolkata') as timestamp
        FROM users u
        LEFT JOIN attempts a ON u.roll_no = a.user_roll AND a.question_id = %s
        ORDER BY u.roll_no ASC
    """, (qid,))
    report = cur.fetchall()
    cur.close(); conn.close()
    return render_template("admin.html", report=report, q_info=q_info, qid=qid)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    # Note: On Render, Gunicorn overrides this entry point.
    app.run(host="0.0.0.0", port=5000)