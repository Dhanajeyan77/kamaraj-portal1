import re
import os
import subprocess
import tempfile
import shutil
import json
import traceback

NSJAIL_BIN = "./bin/nsjail"

def run_code(language, code, test_cases):
    submissions_dir = os.path.join(os.getcwd(), 'temp_submissions')
    os.makedirs(submissions_dir, exist_ok=True)
    tmp_run_dir = tempfile.mkdtemp(dir=submissions_dir)
    results = []
    
    try:
        # --- PHASE 1 & 2: PREPARATION & SANDBOX (UNCHANGED) ---
        run_cmd = []
        if language in ["c", "cpp"]:
            file_ext = "c" if language == "c" else "cpp"
            source_path = os.path.join(tmp_run_dir, f"solution.{file_ext}")
            binary_path = os.path.join(tmp_run_dir, "solution.out")
            with open(source_path, "w") as f:
                f.write(code)
            compiler = "/usr/bin/gcc" if language == "c" else "/usr/bin/g++"
            compile_res = subprocess.run([compiler, source_path, "-o", binary_path], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return {"all_passed": False, "stderr": f"Compile Error:\n{compile_res.stderr}", "summary": "Compilation Failed"}
            run_cmd = ["./solution.out"]

        elif language == "java":
            with open(os.path.join(tmp_run_dir, "Solution.java"), "w") as f:
                f.write(code)
            run_cmd = [
                "/bin/sh", "-c", 
                "export LD_LIBRARY_PATH=/usr/lib/jvm/java-21-openjdk-amd64/lib/server:/usr/lib/jvm/java-21-openjdk-amd64/lib && "
                "/usr/lib/jvm/java-21-openjdk-amd64/bin/javac Solution.java -d /tmp && "
                "/usr/lib/jvm/java-21-openjdk-amd64/bin/java -Xms64m -Xmx256m -cp /tmp Solution"
            ]

        elif language == "python":
            with open(os.path.join(tmp_run_dir, "s.py"), "w") as f:
                f.write(code)
            run_cmd = ["/usr/bin/python3", "s.py"]
            
        elif language == "javascript":
            with open(os.path.join(tmp_run_dir, "solution.js"), "w") as f:
                f.write(code)
            run_cmd = ["/usr/bin/node", "solution.js"]

        selected_mounts = [
            "--bindmount", "/lib:/lib", "--bindmount", "/lib64:/lib64",
            "--bindmount", "/bin:/bin", "--bindmount", "/etc/alternatives:/etc/alternatives",
            "--bindmount", "/etc/ld.so.cache:/etc/ld.so.cache", "--bindmount", "/usr:/usr",
            "--tmpfsmount", "/tmp" 
        ]
        if language == "java":
            selected_mounts += ["--bindmount", "/etc/java-21-openjdk:/etc/java-21-openjdk"]

        config_name = "javascript" if language == "javascript" else language
        
        jail_cmd_base = [
            NSJAIL_BIN, "--config", f"configs/{config_name}.cfg",
        ] + selected_mounts + [
            "--bindmount_ro", f"{tmp_run_dir}:/app", "--cwd", "/app",
            "--disable_clone_newuser", "--"
        ] + run_cmd

        # --- PHASE 3: UPDATED LOOP FOR CRASH SAFETY ---
        for test in test_cases:
            try:
                raw_input = test['input_data']
                formatted_input = raw_input.replace('[', '').replace(']', '').replace(',', ' ')
                formatted_input = " ".join(formatted_input.split())

                process = subprocess.run(
                    jail_cmd_base, 
                    input=formatted_input, 
                    capture_output=True, 
                    text=True, 
                    timeout=15
                )
                
                # Check for return code 137 (SIGKILL/Memory/Time limit)
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
                    "exit_code": process.returncode # 🔥 Added for app.py check
                })
                
                print(f"DEBUG: Language: {language}, ReturnCode: {process.returncode}")

            except subprocess.TimeoutExpired:
                results.append({
                    "passed": False,
                    "input": test['input_data'],
                    "expected": test['expected_output'].strip(),
                    "actual": "TIME LIMIT EXCEEDED",
                    "error": "Process killed after 15s",
                    "exit_code": 124
                })

        all_passed = all(r["passed"] for r in results) if results else False
        return {
            "all_passed": all_passed,
            "test_results": results,
            "summary": "All test cases passed" if all_passed else "Some test cases failed",
            "details": results 
        }

    except Exception as e:
        return {"all_passed": False, "stderr": f"System Error:\n{traceback.format_exc()}", "details": []}
    finally:
        shutil.rmtree(tmp_run_dir, ignore_errors=True)