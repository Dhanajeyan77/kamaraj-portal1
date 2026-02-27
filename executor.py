import re
import os
import subprocess
import tempfile
import shutil
import json
import traceback
import sys

# 🔥 Use Absolute Path for Gunicorn stability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NSJAIL_BIN = os.path.join(BASE_DIR, "bin", "nsjail")

def run_code(language, code, test_cases):
    submissions_dir = os.path.join(BASE_DIR, 'temp_submissions')
    os.makedirs(submissions_dir, exist_ok=True)
    
    tmp_run_dir = tempfile.mkdtemp(dir=submissions_dir)
    # Ensure the directory is accessible to the nsjail process
    os.chmod(tmp_run_dir, 0o777)
    
    results = []
    
    try:
        # --- PHASE 1 & 2: PREPARATION & COMPILATION ---
        run_cmd = []
        if language == "c":
            source_file = "solution.c"
            with open(os.path.join(tmp_run_dir, source_file), "w") as f:
                f.write(code)
            
            run_cmd = [
                "/bin/sh", "-c",
                f"export PATH=$PATH:/usr/bin && "
                f"gcc solution.c -o /tmp/s.out -lm && "
                f"stdbuf -oL /tmp/s.out" 
            ]

        elif language == "cpp":
            source_file = "solution.cpp"
            with open(os.path.join(tmp_run_dir, source_file), "w") as f:
                f.write(code)
            
            run_cmd = [
                "/bin/sh", "-c",
                f"export PATH=$PATH:/usr/bin:/usr/local/bin && "
                f"export CPATH=/usr/include:/usr/local/include && "
                f"/usr/bin/g++ {source_file} -o /tmp/solution.out && "
                f"/tmp/solution.out"
            ]
        elif language == "java":
            source_file_path = os.path.join(tmp_run_dir, "Solution.java")
            with open(source_file_path, "w") as f:
                f.write(code)
            
            java_home = "/usr/lib/jvm/java-21-openjdk-amd64"
            # 🔥 Command template for args[] injection
            java_run_template = (
                f"export LD_LIBRARY_PATH={java_home}/lib/jli:{java_home}/lib:{java_home}/lib/server && "
                f"{java_home}/bin/javac Solution.java && "
                f"{java_home}/bin/java -Xmx512m -cp . Solution "
            )
            run_cmd = []

        elif language == "python":
            with open(os.path.join(tmp_run_dir, "s.py"), "w") as f:
                f.write(code)
            run_cmd = ["/bin/sh", "-c", "/usr/bin/python3 /app/s.py"]

        elif language == "javascript":
            with open(os.path.join(tmp_run_dir, "solution.js"), "w") as f:
                f.write(code)
            run_cmd = ["/usr/bin/node", "/app/solution.js"]

        config_name = "javascript" if language == "javascript" else language
        config_path = os.path.join(BASE_DIR, "configs", f"{config_name}.cfg")
        
        jail_cmd_base = [
            NSJAIL_BIN, 
            "--config", config_path,
            "--bindmount", f"{tmp_run_dir}:/app",
            "--cwd", "/app",
            "--"
        ]

        # --- PHASE 3: EXECUTION LOOP ---
        # --- PHASE 3: EXECUTION LOOP (UPDATED) ---
        for test in test_cases:
            try:
                raw_input = test['input_data']
                formatted_input = str(raw_input).replace('[', '').replace(']', '').replace(',', ' ')
                formatted_input = " ".join(formatted_input.split())

                if language == "java":
                    full_java_command = java_run_template + formatted_input
                    current_jail_cmd = jail_cmd_base + ["/bin/sh", "-c", full_java_command]
                    input_to_pass = None 
                else:
                    current_jail_cmd = jail_cmd_base + run_cmd
                    input_to_pass = formatted_input + "\n"

                # Capture both stdout and stderr for better debugging
                process = subprocess.run(
                    current_jail_cmd, 
                    input=input_to_pass,
                    capture_output=True, 
                    text=True, 
                    timeout=22 
                )

                # Initialize error reporting
                stderr_output = process.stderr.strip() if process.stderr else ""
                
                if process.returncode == 137:
                    actual_raw = "ERROR: Time/Memory Limit Exceeded"
                    is_passed = False
                else:
                    actual_raw = process.stdout if process.stdout else ""
                    expected_raw = test['expected_output']

                    def deep_clean(text):
                        return re.sub(r'[^a-zA-Z0-9:,]', '', text).lower().strip()

                    actual_clean = deep_clean(actual_raw)
                    expected_clean = deep_clean(expected_raw)
                    is_passed = (actual_clean == expected_clean)

                    # Fallback check for numeric equality
                    if not is_passed:
                        a_nums = re.findall(r'\d+', actual_raw)
                        e_nums = re.findall(r'\d+', expected_raw)
                        if a_nums and e_nums and a_nums == e_nums:
                            is_passed = True

                # CRITICAL CHANGE: Include stderr so App.py can find syntax errors
                results.append({
                    "passed": is_passed,
                    "input": test['input_data'],
                    "expected": test['expected_output'].strip(),
                    "actual": actual_raw.strip(),
                    "error": stderr_output, 
                    "exit_code": process.returncode 
                })

            except subprocess.TimeoutExpired:
                results.append({
                    "passed": False,
                    "input": test['input_data'],
                    "expected": test['expected_output'].strip(),
                    "actual": "TIME LIMIT EXCEEDED",
                    "error": "Process killed after timeout",
                    "exit_code": 124
                })

        all_passed = all(r["passed"] for r in results) if results else False
        return {
            "all_passed": all_passed,
            "test_results": results,
            "summary": "All test cases passed" if all_passed else "Some test cases failed",
            "details": results 
        }

    except Exception:
        return {"all_passed": False, "stderr": "An internal system error occurred.", "details": []}
    finally:
        shutil.rmtree(tmp_run_dir, ignore_errors=True)