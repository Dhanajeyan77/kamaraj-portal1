import executor

# ---------------------------------------------------------
# 1. THE INNOCENT PAYLOAD (Bubble Sort - 20 Elements)
# ---------------------------------------------------------
java_code = """
public class Solution {
    public static void main(String[] args) {
        if (args.length == 0) return;
        
        int n = args.length;
        int[] arr = new int[n];
        
        // Parse the 20 elements from args[] to save RAM
        for(int i = 0; i < n; i++){
            arr[i] = Integer.parseInt(args[i]);
        }
        
        // Bubble Sort Algorithm
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
        
        // Print the sorted array
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + (i < n - 1 ? " " : ""));
        }
        System.out.println();
    }
}
"""

# ---------------------------------------------------------
# 2. THE TEST CASES (Input: 20 -> 1 | Expected: 1 -> 20)
# ---------------------------------------------------------
test_cases = [
    {
        "input": "20 19 18 17 16 15 14 13 12 11 10 9 8 7 6 5 4 3 2 1",
        "expected": "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20"
    }
]

print("☕ Firing Java Bubble Sort Payload into the Engine...")

result = executor.run_code(
    language="java",
    code=java_code,
    test_cases=test_cases,
    roll_no="JAVA_TEST_02"
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