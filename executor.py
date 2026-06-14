import re
import os
import subprocess
import shutil
import uuid
import requests
import threading
import time  # For tracking execution speed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NSJAIL_BIN = os.path.join(BASE_DIR, "bin", "nsjail")
MAX_OUTPUT_LENGTH = 10000 

# =====================================================================
# 🚨 BACKGROUND ALERTING SYSTEM
# =====================================================================
def _send_telegram_async(roll_no, issue_type, code):
    bot_token = "8721013528:AAFjFDPGW4COvtZz7nNvhWa5IjT7rH0voaU"
    chat_id = "2073840068"
    code_snippet = code[:200] + "..." if len(code) > 200 else code
    message = f"🚨 KAMARAJ SERVER ALARM 🚨\nRoll No: {roll_no}\nIssue: {issue_type}\nCode:\n{code_snippet}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message}, timeout=3)
    except Exception:
        pass

def send_telegram_alert(roll_no, issue_type, code):
    threading.Thread(target=_send_telegram_async, args=(roll_no, issue_type, code), daemon=True).start()

# =====================================================================
# 🔥 SECURITY LAYER: Comprehensive Pre-execution Keyword Filter
# =====================================================================
def contains_dangerous_code(language, code):
    clean_code_lower = code.replace(" ", "").replace("\t", "").replace("\n", "").replace('"', '').replace("'", "").lower()

    if language == "python":
        blocked_keywords = [
            "importos", "fromos", "importsubprocess", "fromsubprocess", 
            "importsys", "fromsys", "importpty", "frompty", "importimportlib",
            "__import__", "eval(", "exec(", "compile(", "open(", 
            "importsocket", "fromsocket", "importurllib", "fromurllib", 
            "importthreading", "fromthreading", "importmultiprocessing", "frommultiprocessing",
            "os.system", "os.popen", "globals()", "locals()"
        ]
        return any(bad_word in clean_code_lower for bad_word in blocked_keywords)

    elif language == "java":
        blocked_keywords = [
            "java.lang.runtime", "processbuilder", "system.getenv",
            "java.io.file", "filereader", "filewriter", "java.net", 
            "httpurlconnection", "java.lang.reflect", "system.exit",
            "runtime.getruntime", "socket(", "serversocket(", "urlconnection"
        ]
        return any(bad_word in clean_code_lower for bad_word in blocked_keywords)

    elif language in ["c", "cpp"]:
        blocked_keywords = [
            "system(", "exec(", "execl(", "execle(", "execv(", "execvp(", 
            "fork(", "vfork(", "clone(", "popen(", "fopen(", "freopen(", "open(", 
            "socket(", "connect(", "bind(", "listen(", "pthread_create(", 
            "asm(", "__asm__("
        ]
        return any(bad_word in clean_code_lower for bad_word in blocked_keywords)

    elif language == "javascript":
        blocked_keywords = [
            "require('child_process')", "require('fs')", "require('os')", 
            "require('net')", "require('http')", "require('https')", 
            "eval(", "process.exit", "process.env", "child_process.exec", 
            "child_process.spawn"
        ]
        return any(bad_word in clean_code_lower for bad_word in blocked_keywords)
    
    return False 

# =====================================================================
# ⚙️ MAIN EXECUTION PIPELINE
# =====================================================================
def run_code(language, code, test_cases, roll_no="UNKNOWN"):
    if contains_dangerous_code(language, code):
        send_telegram_alert(roll_no, "Blocked Keyword Attempted", code)
        return {
            "all_passed": False,
            "test_results": [{"passed": False, "input": "N/A", "expected": "N/A", "actual": "ERROR: Security Violation", "error": "Blocked by pre-execution filter", "exit_code": 403, "time_ms": 0}],
            "summary": "Security Violation Detected",
            "details": [] 
        }

    submissions_dir = os.path.join(BASE_DIR, 'temp_submissions')
    os.makedirs(submissions_dir, exist_ok=True)
    
    unique_run_id = f"{roll_no}_{uuid.uuid4().hex[:8]}"
    tmp_run_dir = os.path.join(submissions_dir, unique_run_id)
    os.makedirs(tmp_run_dir, exist_ok=True)
    os.chmod(tmp_run_dir, 0o777)
    
    results = []
    
    try:
        run_cmd = []
        if language == "c":
            with open(os.path.join(tmp_run_dir, "solution.c"), "w") as f:
                f.write(code)
            run_cmd = ["/bin/sh", "-c", "export PATH=$PATH:/usr/bin && gcc solution.c -o /tmp/s.out -lm && stdbuf -oL /tmp/s.out"]

        elif language == "cpp":
            with open(os.path.join(tmp_run_dir, "solution.cpp"), "w") as f:
                f.write(code)
            run_cmd = ["/bin/sh", "-c", "export PATH=$PATH:/usr/bin:/usr/local/bin && export CPATH=/usr/include:/usr/local/include && /usr/bin/g++ solution.cpp -o /tmp/solution.out && /tmp/solution.out"]
            
        elif language == "java":
            match = re.search(r'public\s+class\s+([A-Za-z0-9_]+)', code)
            java_class_name = match.group(1) if match else "Solution"
            
            with open(os.path.join(tmp_run_dir, f"{java_class_name}.java"), "w") as f:
                f.write(code)
            
            java_home = "/usr/lib/jvm/java-21-openjdk-amd64"
            with open(os.path.join(tmp_run_dir, "run.sh"), "w") as f:
                f.write(f"#!/bin/sh\n")
                f.write(f"set -e\n") 
                f.write(f"export LD_LIBRARY_PATH={java_home}/lib/jli:{java_home}/lib:{java_home}/lib/server\n")
                f.write(f"{java_home}/bin/javac -J-Xmx256m -J-Xms64m {java_class_name}.java\n")
                f.write(f"{java_home}/bin/java -Xmx256m -Xms64m -XX:MaxMetaspaceSize=128m -XX:+UseSerialGC -Xss512k -cp . {java_class_name} \"$@\"\n")
            
            os.chmod(os.path.join(tmp_run_dir, "run.sh"), 0o777)
            run_cmd = ["/app/run.sh"]
        
        elif language == "python":
            with open(os.path.join(tmp_run_dir, "s.py"), "w") as f:
                f.write(code)
            run_cmd = ["/usr/bin/python3", "-u", "/app/s.py"]

        elif language == "javascript":
            with open(os.path.join(tmp_run_dir, "solution.js"), "w") as f:
                f.write(code)
            run_cmd = ["/usr/bin/node", "/app/solution.js"]

        config_path = os.path.join(BASE_DIR, "configs", f"{language}.cfg")
        
        jail_cmd_base = [
            NSJAIL_BIN, 
            "-q",
            "--use_cgroupv2",
            "--cgroup_mem_max", "536870912",   
            "--cgroup_pids_max", "40",         
            "--config", config_path,
            "--bindmount", f"{tmp_run_dir}:/app",
            "--cwd", "/app",
            "--"
        ]

        for test in test_cases:
            try:
                # 🔥 THE FIX: Seamlessly handle both dictionary formats
                raw_input = test.get("input_data", test.get("input", ""))
                expected_raw = test.get("expected_output", test.get("expected", ""))
                
                formatted_input = str(raw_input).replace('[', '').replace(']', '').replace(',', ' ')
                formatted_input = " ".join(formatted_input.split())

                if language == "java":
                    current_jail_cmd = jail_cmd_base + run_cmd + formatted_input.split()
                    input_to_pass = None 
                else:
                    current_jail_cmd = jail_cmd_base + run_cmd
                    input_to_pass = formatted_input + "\n"

                start_time = time.perf_counter()

                process = subprocess.run(
                    current_jail_cmd, 
                    input=input_to_pass,
                    capture_output=True, 
                    text=True, 
                    timeout=7
                )

                exec_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

                stderr_output = (process.stderr[:MAX_OUTPUT_LENGTH].strip() + "\n...[TRUNCATED]") if process.stderr and len(process.stderr) > MAX_OUTPUT_LENGTH else (process.stderr.strip() if process.stderr else "")
                raw_stdout = process.stdout if process.stdout else ""
                actual_raw = (raw_stdout[:MAX_OUTPUT_LENGTH] + "\n...[TRUNCATED]") if len(raw_stdout) > MAX_OUTPUT_LENGTH else raw_stdout

                if language == "java" and "OutOfMemoryError" in stderr_output:
                    actual_raw = "ERROR: Memory Limit Exceeded (Java Heap limit)"
                    is_passed = False
                    send_telegram_alert(roll_no, "Java Memory Leak! Exceeded 512MB", code)
                    results.append({"passed": False, "input": raw_input, "expected": expected_raw, "actual": actual_raw, "error": stderr_output, "exit_code": 1, "time_ms": exec_time_ms})
                    break

                elif process.returncode == 137 or "MemoryError" in stderr_output:
                    actual_raw = "ERROR: Time/Memory Limit Exceeded"
                    is_passed = False
                    send_telegram_alert(roll_no, f"{language.upper()} Time/Memory Limit Hit", code)
                    results.append({"passed": False, "input": raw_input, "expected": expected_raw, "actual": actual_raw, "error": stderr_output, "exit_code": 137, "time_ms": exec_time_ms})
                    break

                elif process.returncode == 152:
                    actual_raw = "ERROR: CPU Time Limit Exceeded (Possible Infinite Loop or Fork Bomb)"
                    is_passed = False
                    send_telegram_alert(roll_no, "CPU Limit / Fork Bomb Blocked!", code)
                    results.append({"passed": False, "input": raw_input, "expected": expected_raw, "actual": actual_raw, "error": stderr_output, "exit_code": 152, "time_ms": exec_time_ms})
                    break

                elif process.returncode == 139:
                    actual_raw = "ERROR: Segmentation Fault (Memory Access Error)"
                    is_passed = False
                    results.append({"passed": False, "input": raw_input, "expected": expected_raw, "actual": actual_raw, "error": stderr_output, "exit_code": 139, "time_ms": exec_time_ms})
                    break
                    
                elif process.returncode != 0:
                    actual_raw = f"RUNTIME ERROR (Exit Code {process.returncode})\n" + actual_raw
                    is_passed = False
                else:
                    def deep_clean(text):
                        return re.sub(r'[^a-zA-Z0-9:,]', '', text).lower().strip()

                    is_passed = (deep_clean(actual_raw) == deep_clean(expected_raw))

                    if not is_passed:
                        a_nums = re.findall(r'\d+', actual_raw)
                        e_nums = re.findall(r'\d+', expected_raw)
                        if a_nums and e_nums and a_nums == e_nums:
                            is_passed = True

                results.append({
                        "passed": is_passed,
                        "input": raw_input,
                        "expected": expected_raw.strip(),
                        "actual": actual_raw.strip(),
                        "error": stderr_output, 
                        "exit_code": process.returncode,
                        "time_ms": exec_time_ms
                    })

            except subprocess.TimeoutExpired:
                results.append({
                    "passed": False,
                    "input": test.get("input_data", test.get("input", "N/A")),
                    "expected": test.get("expected_output", test.get("expected", "N/A")).strip(),
                    "actual": "TIME LIMIT EXCEEDED",
                    "error": "Process killed after 7 second timeout",
                    "exit_code": 124,
                    "time_ms": 7000
                })
                break

        all_passed = all(r["passed"] for r in results) if results else False
        return {
            "all_passed": all_passed,
            "test_results": results,
            "summary": "All test cases passed" if all_passed else "Some test cases failed",
            "details": results 
        }

    except Exception as e:
        logging.error(f"System Error for {roll_no}: {str(e)}")
        return {"all_passed": False, "test_results": [], "summary": "System Error", "details": []}
    finally:
        shutil.rmtree(tmp_run_dir, ignore_errors=True)