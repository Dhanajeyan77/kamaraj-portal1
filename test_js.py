import executor

# ---------------------------------------------------------
# 1. THE JAVASCRIPT PAYLOAD
# ---------------------------------------------------------
js_code = """
const fs = require('fs');

// Try to hack the server by reading a secret file
try {
    const secret = fs.readFileSync('/etc/passwd', 'utf8');
    console.log("HACKED! I read your file!");
} catch (error) {
    // If the jail works, it will fail to read it.
    console.log("1"); 
}
"""

test_cases = [
    {"input": "1", "expected": "1"}
]

print("🚀 Firing JavaScript Payload into the Engine...")

result = executor.run_code(
    language="javascript",
    code=js_code,
    test_cases=test_cases,
    roll_no="JS_TEST_01"
)

# ---------------------------------------------------------
# 3. PRINT RESULTS
# ---------------------------------------------------------
print("\n=== EXECUTION RESULT ===")
print(f"Status: {result['summary']}")
print(f"Output: {result['test_results'][0]['actual']}")
print(f"Exit Code: {result['test_results'][0]['exit_code']}")
if 'time_ms' in result['test_results'][0]:
    print(f"Execution Time: {result['test_results'][0]['time_ms']} ms")
if 'error' in result['test_results'][0] and result['test_results'][0]['error']:
    print(f"Hidden NsJail Log:\n{result['test_results'][0]['error']}")
