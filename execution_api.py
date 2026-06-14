from flask import Flask, request, jsonify
import queue_worker  # 🔥 UPGRADE 1: Import the queue, NOT the executor!
import os

app = Flask(__name__)

# 🔥 UPGRADE 4: Security Token. The main Kamaraj web server must send this exact key!
API_SECRET = "kamaraj-engine-2026"

@app.route('/run', methods=['POST'])
def run_code():
    # Security Layer: Reject requests that don't have the secret key
    if request.headers.get("X-API-Key") != API_SECRET:
        return jsonify({"status": "error", "message": "Unauthorized execution attempt"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
        
    code = data.get('code')
    language = data.get('language')
    test_cases = data.get('test_cases', [])
    roll_no = data.get('roll_no', 'UNKNOWN')
    
    try:
        # 🔥 UPGRADE 1: Send the job to the Queue instead of running it instantly!
        job_id = queue_worker.submit_job(
            user=roll_no, 
            code=code, 
            language=language, 
            test_cases=test_cases
        )
        
        # 🔥 UPGRADE 2: Handle Spam Protection
        if job_id == "SPAM_BLOCK":
            return jsonify({"status": "error", "message": "Please wait 3 seconds between submissions."}), 429
        
        # 🔥 UPGRADE 1 (Cont): Wait patiently for the background worker to finish the job
        results = queue_worker.get_result(job_id, language=language)
        
        return jsonify({"status": "success", "results": results}), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔥 UPGRADE 3: Admin Dashboard Health Check
@app.route('/health', methods=['GET'])
def health_check():
    # Security Layer
    if request.headers.get("X-API-Key") != API_SECRET:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
        
    metrics = queue_worker.get_engine_metrics()
    return jsonify({"status": "online", "metrics": metrics}), 200

if __name__ == '__main__':
    # Keep debug=False! If debug=True, Flask reloads twice and creates TWO queue systems!
    app.run(host='0.0.0.0', port=5000, debug=False)