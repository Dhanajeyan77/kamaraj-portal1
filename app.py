from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import multiprocessing
import io
from contextlib import redirect_stdout

app = Flask(__name__)
app.secret_key = "kamaraj_college_2025"
DATABASE = "database/users.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def execute_user_code(user_code, expected_answer, result_dict):
    """Executes code using standard Python with a string buffer."""
    f = io.StringIO()
    try:
        # We run in a clean local dictionary to avoid variable conflicts
        local_vars = {}
        # Redirect terminal output to our string buffer 'f'
        with redirect_stdout(f):
            exec(user_code, {"__builtins__": __builtins__}, local_vars)
        
        actual_output = f.getvalue().strip()
        expected_output = str(expected_answer).strip()
        
        result_dict['output'] = actual_output
        # Case-insensitive comparison for student fairness
        result_dict['is_correct'] = (actual_output.lower() == expected_output.lower())
    except Exception as e:
        # If the student has a syntax error, we send it to the console
        result_dict['error'] = str(e)

@app.route("/")
def index():
    if "user" in session: return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].upper()
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE roll_no=? AND password=?", (username, password)).fetchone()
        conn.close()
        if user:
            session["user"] = username
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/home")
def home():
    if "user" not in session: return redirect(url_for("login"))
    return render_template("home.html", user=session["user"])

@app.route("/questions")
def questions():
    if "user" not in session: return redirect(url_for("login"))
    conn = get_db_connection()
    qs = conn.execute("SELECT * FROM questions").fetchall()
    conn.close()
    return render_template("questions.html", questions=qs)

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question_detail(qid):
    if "user" not in session: return redirect(url_for("login"))
    output = ""
    conn = get_db_connection()
    q = conn.execute("SELECT * FROM questions WHERE id=?", (qid,)).fetchone()

    if request.method == "POST":
        user_code = request.form["user_code"]
        manager = multiprocessing.Manager()
        result_dict = manager.dict()
        
        # Protects your Ubuntu OS from infinite loops
        p = multiprocessing.Process(target=execute_user_code, args=(user_code, q['expected_output'], result_dict))
        p.start()
        p.join(timeout=3) # 3-second limit
        
        if p.is_alive():
            p.terminate()
            output = "❌ Timeout Error: Your code took too long to run. Check for infinite loops!"
        elif 'error' in result_dict:
            output = f"⚠️ Python Error: {result_dict['error']}"
        else:
            actual = result_dict.get('output', "")
            if result_dict.get('is_correct'):
                output = f"Result: {actual}\n\n✅ CORRECT! Well done."
                conn.execute("INSERT OR REPLACE INTO attempts (user_roll, question_id, status, code) VALUES (?, ?, ?, ?)",
                             (session["user"], qid, "Completed", user_code))
                conn.commit()
            else:
                output = f"Result: {actual}\n\n❌ INCORRECT. Double check spelling and try again!"
    
    conn.close()
    return render_template("question_detail.html", question=q, output=output)
@app.route("/solutions")
def solutions():
    # 1. Security: Ensure the user is logged in
    if "user" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    # 2. Fetch all 'Completed' attempts for this specific roll number
    # We JOIN with questions to show the date of each task
    user_solutions = conn.execute("""
        SELECT a.code, a.timestamp, q.date, q.content 
        FROM attempts a 
        JOIN questions q ON a.question_id = q.id 
        WHERE a.user_roll = ? AND a.status = 'Completed'
        ORDER BY q.date DESC
    """, (session["user"],)).fetchall()
    
    conn.close()
    return render_template("solutions.html", solutions=user_solutions)
@app.route("/admin/<int:qid>")
def admin_dashboard(qid):
    # 1. Security Check
    if "user" not in session: 
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    user = conn.execute("SELECT is_admin FROM users WHERE roll_no=?", (session["user"],)).fetchone()
    
    if not user or user['is_admin'] != 1:
        conn.close()
        return "Access Denied", 403

    # 2. Fetch specific question info
    q_info = conn.execute("SELECT date, content FROM questions WHERE id=?", (qid,)).fetchone()

    # 3. Fetch report for ALL students for THIS specific question
    report = conn.execute("""
        SELECT users.roll_no, users.name, attempts.status, attempts.timestamp 
        FROM users 
        LEFT JOIN attempts ON users.roll_no = attempts.user_roll 
        AND attempts.question_id = ?
    """, (qid,)).fetchall()
    
    conn.close()
    return render_template("admin.html", report=report, q_info=q_info, qid=qid)
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)