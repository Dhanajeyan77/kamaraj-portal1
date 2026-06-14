import executor

# ---------------------------------------------------------
# 1. THE INNOCENT PAYLOAD (C Language)
# ---------------------------------------------------------
c_code = """
#include <stdio.h>

int main() {
    int num;
    if (scanf("%d", &num) == 1) {
        printf("%d\\n", num);
    }
    return 0;
}
"""

test_cases = [
    {"input": "1", "expected": "1"}
]

print("⚙️ Firing C Payload into the Engine...")

result = executor.run_code(
    language="c",
    code=c_code,
    test_cases=test_cases,
    roll_no="C_TEST_01"
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
