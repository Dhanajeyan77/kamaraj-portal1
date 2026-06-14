import queue # 🔥 FIX 1: Added missing import
import threading
import uuid
import time
import logging
import os # 🔥 NEW: For checking real RAM
from datetime import datetime, timedelta
from executor import run_code
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

live_audit_log = deque(maxlen=20)
job_queue = queue.Queue()
results = {}
job_events = {} 
job_timestamps = {} 
results_lock = threading.Lock()

# 🔥 UPGRADE 2: Spam Protection Dictionary
user_last_submit = {}

MAX_PARALLEL = 5 

def worker(worker_id):
    """Hardened worker with Auto-Retry and explicit error signaling."""
    while True:
        # 🔥 UPGRADE 1: Unpack retries
        job_id, payload, retries = job_queue.get()
        user_roll = payload.pop('user', 'Unknown')
        lang = payload.get('language', 'Unknown')
        
        logging.info(f"🚀 [Worker {worker_id}] Starting Job {job_id} for {user_roll} (Attempt {retries + 1})")
        
        try:
            payload['roll_no'] = user_roll
            result = run_code(**payload)
            
            test_results = result.get("test_results", [])
            first_fail = next((r for r in test_results if not r.get("passed")), None)
            exit_code = first_fail.get("exit_code", 0) if first_fail else 0

            status = "✅ Success" if result.get("all_passed") else "❌ Failed"
            if exit_code == 403: status = "🚨 SECURITY VIOLATION"
            elif exit_code == 152: status = "🚨 FORK BOMB / CPU"
            elif exit_code == 137: status = "📉 MEMORY LIMIT"
            elif exit_code == 124: status = "🕒 TIMEOUT"
            elif exit_code == 255: status = "⚙️ NSJAIL SYSTEM ERROR"

            live_audit_log.appendleft({
                "time": datetime.now().strftime("%H:%M:%S"),
                "roll": user_roll,
                "lang": lang,
                "status": status,
                "danger": exit_code in [403, 152, 137, 255] 
            })
            
            # 🔥 UPGRADE 1: Auto-Retry for transient VM failures (Exit Code 255/500)
            if exit_code in [255, 500] and retries < 1:
                logging.warning(f"⚠️ [Worker {worker_id}] VM Glitch on {job_id}. Retrying silently...")
                job_queue.put((job_id, payload, retries + 1))
                job_queue.task_done()
                continue # Skip saving results and let the next worker try

            with results_lock:
                results[job_id] = result
                job_timestamps[job_id] = datetime.now()
        
        except Exception as e:
            logging.error(f"❌ [Worker {worker_id}] CRITICAL ERROR: {str(e)}")
            with results_lock:
                results[job_id] = {
                    "all_passed": False, 
                    "summary": "Execution Engine Error",
                    "test_results": [],
                    "exit_code": 500 
                }
        finally:
            if job_id in job_events:
                job_events[job_id].set()
            
            job_queue.task_done()
            logging.info(f"✅ [Worker {worker_id}] Finished Job {job_id}")

def cleanup_zombie_jobs():
    """Background thread to remove abandoned results and clear spam filters."""
    while True:
        time.sleep(60) 
        now = datetime.now()
        with results_lock:
            to_remove = [jid for jid, ts in job_timestamps.items() if now - ts > timedelta(minutes=5)]
            for jid in to_remove:
                results.pop(jid, None)
                job_events.pop(jid, None)
                job_timestamps.pop(jid, None)
            
            # Clear old spam protection entries to free up memory
            stale_users = [user for user, ts in user_last_submit.items() if (now - ts).total_seconds() > 10]
            for user in stale_users:
                user_last_submit.pop(user, None)

def get_queue_status():
    return {
        "pending_jobs": job_queue.qsize(),
        "active_workers": MAX_PARALLEL,
        "completed_results_in_memory": len(results)
    }

for i in range(MAX_PARALLEL):
    threading.Thread(target=worker, args=(i,), daemon=True).start()

threading.Thread(target=cleanup_zombie_jobs, daemon=True).start()

def submit_job(user, code, language, test_cases):
    """Adds a job to the queue with Spam Protection."""
    
    # 🔥 UPGRADE 2: Spam Protection Check (3 seconds cooldown)
    now = datetime.now()
    if user in user_last_submit:
        time_since_last = (now - user_last_submit[user]).total_seconds()
        if time_since_last < 3.0:
            return "SPAM_BLOCK"
            
    user_last_submit[user] = now

    job_id = str(uuid.uuid4())
    job_events[job_id] = threading.Event()
    
    # Notice we pass '0' at the end for retries!
    job_queue.put((job_id, {
        "user": user,
        "language": language, 
        "code": code, 
        "test_cases": test_cases
    }, 0)) 
    
    return job_id

def get_result(job_id, language="python"):
    """Waits for the background worker to finish."""
    event = job_events.get(job_id)
    if event:
        # 🔥 UPGRADE 3: Dynamic Timeouts. Java gets 20s, Python/C only need 10s.
        timeout_limit = 20 if language == "java" else 10
        event.wait(timeout=timeout_limit)
    
    with results_lock:
        res = results.pop(job_id, {"all_passed": False, "summary": "System Timeout"})
        job_events.pop(job_id, None)
        job_timestamps.pop(job_id, None)
        return res
def get_engine_metrics():
    """Returns REAL-TIME data for the Admin Dashboard."""
    try:
        real_ram = int(os.popen("free -m | awk 'NR==2{print $3}'").read().strip())
    except:
        real_ram = 0 

    with results_lock:
        return {
            "queue_depth": job_queue.qsize(),
            "cached_results": len(results),
            "worker_count": MAX_PARALLEL,
            "memory_usage_mb": real_ram,
            "audit_log": list(live_audit_log), # 🔥 NEW: Send the log!
            "server_time": datetime.now().strftime("%H:%M:%S") # 🔥 NEW: Send the time!
        }