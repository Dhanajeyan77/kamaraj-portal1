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
            with open(os.path.join(tmp_run_dir, "Solution.java"), "w") as f:
                f.write(code)
            
            java_bin = "/usr/lib/jvm/java-21-openjdk-amd64/bin"
            java_lib = "/usr/lib/jvm/java-21-openjdk-amd64/lib"
            
            run_cmd = [
                "/bin/sh", "-c", 
                f"export LD_LIBRARY_PATH={java_lib}/server:{java_lib} && "
                f"{java_bin}/javac Solution.java -d /tmp && "
                f"{java_bin}/java -Xmx256m -cp /tmp Solution"
            ]

        elif language == "python":
            with open(os.path.join(tmp_run_dir, "s.py"), "w") as f:
                f.write(code)
            run_cmd = ["/bin/sh", "-c", "/usr/bin/python3 /app/s.py"]

        elif language == "javascript":
            with open(os.path.join(tmp_run_dir, "solution.js"), "w") as f:
                f.write(code)
            run_cmd = ["/usr/bin/node", "/app/solution.js"]

        # Determine config file
        config_name = "javascript" if language == "javascript" else language
        config_path = os.path.join(BASE_DIR, "configs", f"{config_name}.cfg")
        
        jail_cmd_base = [
            NSJAIL_BIN, 
            "--config", config_path,
            "--bindmount_ro", f"{tmp_run_dir}:/app",
            "--cwd", "/app",
            "--"
        ] + run_cmd

        # --- PHASE 3: EXECUTION LOOP (CLEANED) ---
        for test in test_cases:
            try:
                raw_input = test['input_data']
                formatted_input = str(raw_input).replace('[', '').replace(']', '').replace(',', ' ')
                formatted_input = " ".join(formatted_input.split())

                process = subprocess.run(
                    jail_cmd_base, 
                    input=formatted_input, 
                    capture_output=True, 
                    text=True, 
                    timeout=22 
                )

                if process.returncode == 137:
                    actual_raw = "ERROR: Time/Memory Limit Exceeded (Killed)"
                    is_passed = False
                else:
                    actual_raw = process.stdout if process.stdout else ""
                    expected_raw = test['expected_output']

                    def deep_clean(text):
                        return re.sub(r'[^a-zA-Z0-9:,]', '', text).lower().strip()

                    actual_clean = deep_clean(actual_raw)
                    expected_clean = deep_clean(expected_raw)
                    is_passed = (actual_clean == expected_clean)

                    if not is_passed:
                        a_nums = re.findall(r'\d+', actual_raw)
                        e_nums = re.findall(r'\d+', expected_raw)
                        if a_nums and e_nums:
                            is_passed = (a_nums == e_nums)

                results.append({
                    "passed": is_passed,
                    "input": test['input_data'],
                    "expected": test['expected_output'].strip(),
                    "actual": actual_raw.strip(),
                    "error": process.stderr,
                    "exit_code": process.returncode 
                })
                
            except subprocess.TimeoutExpired:
                # 🔥 We keep only critical system warnings
                print(f"CRITICAL: Timeout triggered for {language}", file=sys.stderr)
                sys.stderr.flush()
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
        return {"all_passed": False, "stderr": f"System Error:\n{traceback.format_exc()}", "details": []}
    finally:
        shutil.rmtree(tmp_run_dir, ignore_errors=True)