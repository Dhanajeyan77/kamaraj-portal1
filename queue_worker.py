import queue
import threading
import uuid
import time
import logging
from datetime import datetime, timedelta
from executor import run_code

# Thread-safe storage
job_queue = queue.Queue()
results = {}
job_events = {} 
job_timestamps = {} # 🔥 Track when jobs were created for cleanup
results_lock = threading.Lock()

# 8GB RAM Protection: Allow 5 parallel jails at a time
MAX_PARALLEL = 5 

def worker():
    """Background worker that pulls jobs and signals completion via Events."""
    while True:
        job_id, payload = job_queue.get()
        try:
            # Execute the code via NsJail in executor.py
            result = run_code(**payload)
            
            with results_lock:
                results[job_id] = result
                # Timestamp when the result was finished
                job_timestamps[job_id] = datetime.now()
            
            # 🔥 The Handshake: Wake up the waiting Flask route
            if job_id in job_events:
                job_events[job_id].set()
        
        except Exception as e:
            logging.error(f"Worker Error for job {job_id}: {str(e)}")
            with results_lock:
                results[job_id] = {"all_passed": False, "summary": "System Error"}
                job_timestamps[job_id] = datetime.now()
            if job_id in job_events:
                job_events[job_id].set()
        finally:
            job_queue.task_done()

# --- ADDITIONAL FUNCTIONS (DOES NOT AFFECT WORKER LOGIC) ---

def cleanup_zombie_jobs():
    """Background thread to remove results that were never collected by the frontend."""
    while True:
        time.sleep(60) # Run every minute
        now = datetime.now()
        with results_lock:
            # Find jobs older than 5 minutes
            to_remove = [
                jid for jid, ts in job_timestamps.items() 
                if now - ts > timedelta(minutes=5)
            ]
            for jid in to_remove:
                results.pop(jid, None)
                job_events.pop(jid, None)
                job_timestamps.pop(jid, None)
                logging.info(f"Cleaned up zombie job: {jid}")

def get_queue_status():
    """Returns the current state of the engine for an Admin Dashboard."""
    return {
        "pending_jobs": job_queue.qsize(),
        "active_workers": MAX_PARALLEL,
        "completed_results_in_memory": len(results)
    }

# --- END ADDITIONAL FUNCTIONS ---

# Start background workers immediately upon import
for _ in range(MAX_PARALLEL):
    threading.Thread(target=worker, daemon=True).start()

# Start the cleanup thread
threading.Thread(target=cleanup_zombie_jobs, daemon=True).start()

def submit_job(user, code, language, test_cases):
    """Adds a job to the queue and returns a tracking ID."""
    job_id = str(uuid.uuid4())
    job_events[job_id] = threading.Event()
    # We don't timestamp here because the worker handles it once finished
    job_queue.put((job_id, {
        "language": language, 
        "code": code, 
        "test_cases": test_cases
    }))
    return job_id

def get_result(job_id):
    """Waits for the background worker to signal that the result is ready."""
    event = job_events.get(job_id)
    if event:
        # Wait up to 20s. NsJail is fast, but Java/C++ compilation takes time.
        event.wait(timeout=20)
    
    with results_lock:
        # Retrieve and clear memory to prevent RAM bloat
        res = results.pop(job_id, {"all_passed": False, "summary": "System Timeout"})
        job_events.pop(job_id, None)
        job_timestamps.pop(job_id, None)
        return res