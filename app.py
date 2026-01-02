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
import subprocess
import os
import io
from contextlib import redirect_stdout

def execute_user_code(user_code, expected_answer, result_dict, lang='python'):
    expected_output = str(expected_answer).strip().lower()
    
    # --- PYTHON EXECUTION ---
    if lang == 'python':
        f = io.StringIO()
        try:
            local_vars = {}
            with redirect_stdout(f):
                # Using exec for internal Python execution
                exec(user_code, {"__builtins__": __builtins__}, local_vars)
            actual_output = f.getvalue().strip()
            result_dict['output'] = actual_output
            result_dict['is_correct'] = actual_output.lower() == expected_output
        except Exception as e:
            result_dict['error'] = f"Python Error: {str(e)}"
            
    # --- JAVA EXECUTION ---
    elif lang == 'java':
        java_file = "Solution.java"
        class_file = "Solution.class"
        try:
            # 1. Write the student's code to a file
            with open(java_file, "w") as f:
                f.write(user_code)
            
            # 2. Compile the Java file (requires javac installed)
            compile_process = subprocess.run(
                ['javac', java_file], 
                capture_output=True, 
                text=True
            )
            
            if compile_process.returncode != 0:
                result_dict['error'] = "Compilation Error:\n" + compile_process.stderr
                return

            # 3. Execute the compiled class (requires java installed)
            run_process = subprocess.run(
                ['java', 'Solution'], 
                capture_output=True, 
                text=True, 
                timeout=3 # Matches your Python timeout
            )
            
            actual_output = run_process.stdout.strip()
            result_dict['output'] = actual_output
            result_dict['is_correct'] = actual_output.lower() == expected_output
            
        except subprocess.TimeoutExpired:
            result_dict['error'] = "Timeout Error: Your Java code took too long to run!"
        except Exception as e:
            result_dict['error'] = f"Java Execution Error: {str(e)}"
        finally:
            # Cleanup: Delete the .java and .class files after execution
            if os.path.exists(java_file):
                os.remove(java_file)
            if os.path.exists(class_file):
                os.remove(class_file)

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
        
        # 1. Capture the language choice from the dropdown
        selected_lang = request.form.get("lang_choice", "python") 
        
        manager = multiprocessing.Manager()
        result_dict = manager.dict()
        
        # 2. Pass the selected_lang to the execution function
        p = multiprocessing.Process(
            target=execute_user_code, 
            args=(user_code, q['expected_output'], result_dict, selected_lang)
        )
        p.start()
        p.join(timeout=4) # Increased to 4s because Java compilation takes a second

        if p.is_alive():
            p.terminate()
            output = "❌ Timeout Error: Code took too long!"
        elif 'error' in result_dict:
            # 3. Make the error message dynamic (Python or Java)
            output = f"⚠️ {result_dict['error']}"
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
    
    # Pass selected_lang back to template so the dropdown stays on 'java' after refresh
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