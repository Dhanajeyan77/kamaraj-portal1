import psycopg2 # Changed from sqlite3
from datetime import datetime, timedelta

def setup_curriculum():
    # PostgreSQL Connection to Supabase
    conn = psycopg2.connect(
        host="db.lgdoppdnlkdrfixxulyb.supabase.co",
        database="postgres",
        user="postgres",
        password="Dhanajeyan@17",
        port=5432,
        sslmode="require"
    )
    cursor = conn.cursor()

    # Clean the existing database to avoid duplicates
    cursor.execute("DELETE FROM questions")
    # Complete 90-Question Bank
    challenges = [
        # --- PHASE 1: NUMBER THEORY & SERIES (DAYS 1-30) ---
        ("Problem 1: Mixed Power Series\nConcept: Pattern identification in interleaved sequences.\nStrategy: Identify two series: 2^(n/2) for odd positions and 3^(n/2-1) for even positions.\nSample Input: 5\nSample Output: 4", "Actual Input: 14", "729"),
        ("Problem 2: Digital Persistence\nConcept: Recursive multiplication. Measures the steps to reach a single-digit root.\nStrategy: While number > 9, multiply its digits and increment step count.\nSample Input: 39\nSample Output: 3", "Actual Input: 77", "4"),
        ("Problem 3: Strong Number\nConcept: Digit factorial summation.\nStrategy: Sum the factorials of each digit and compare to the original number.\nSample Input: 145\nSample Output: True", "Actual Input: 40585", "True"),
        ("Problem 4: Base-6 Conversion\nConcept: Positional number systems.\nStrategy: Use the division-remainder method with 6 as the divisor.\nSample Input: 100\nSample Output: 244", "Actual Input: 2025", "13213"),
        ("Problem 5: Smallest Cube Multiplier\nConcept: Prime factorization exponents.\nStrategy: Ensure every prime exponent is a multiple of 3.\nSample Input: 12\nSample Output: 18", "Actual Input: 675", "5"),
        ("Problem 6: Proper Divisor Sum\nConcept: Aliquot sums in number theory.\nStrategy: Iterate up to sqrt(N) to find all divisors excluding N.\nSample Input: 12\nSample Output: 16", "Actual Input: 220", "284"),
        ("Problem 7: Harshad Number\nConcept: Integer divisibility properties.\nStrategy: Check if N is divisible by the sum of its digits.\nSample Input: 18\nSample Output: True", "Actual Input: 1729", "True"),
        ("Problem 8: Array GCD\nConcept: Greatest Common Divisor for multiple inputs.\nStrategy: Apply Euclidean algorithm iteratively across the array.\nSample Input: [12, 24]\nSample Output: 12", "Actual Input: [48, 144, 168]", "24"),
        ("Problem 9: Fibonacci (Iterative)\nConcept: Linear recurrence relations.\nStrategy: Use two variables to store previous terms to achieve O(n) space.\nSample Input: 10\nSample Output: 55", "Actual Input: 20", "6765"),
        ("Problem 10: Trailing Zeros in N!\nConcept: Legendre's Formula.\nStrategy: Count total factors of 5 in the range 1 to N.\nSample Input: 10\nSample Output: 2", "Actual Input: 100", "24"),
        ("Problem 11: Total Set Bits\nConcept: Binary representation analysis.\nStrategy: Use bitwise shifts or recursion to count '1's from 1 to N.\nSample Input: 3\nSample Output: 4", "Actual Input: 7", "12"),
        ("Problem 12: Single Element in Triplets\nConcept: Bitwise XOR and masking.\nStrategy: Track bits that appear once, twice, and thrice.\nSample Input: [2,2,3,2]\nSample Output: 3", "Actual Input: [5, 5, 8, 5]", "8"),
        ("Problem 13: Kaprekar Number\nConcept: Square-and-split logic.\nStrategy: Split the square of N into two parts; check if their sum equals N.\nSample Input: 45\nSample Output: True", "Actual Input: 297", "True"),
        ("Problem 14: Modular Exponentiation\nConcept: Cryptographic power calculation.\nStrategy: Use binary exponentiation (A^B % C) to avoid overflow.\nSample Input: 2, 10, 7\nSample Output: 2", "Actual Input: 5, 3, 13", "8"),
        ("Problem 15: Modular Inverse\nConcept: Extended Euclidean Algorithm.\nStrategy: Find x such that (A * x) % M == 1.\nSample Input: 3, 11\nSample Output: 4", "Actual Input: 15, 26", "7"),
        ("Problem 16: Goldbach Check\nConcept: Prime sum theory.\nStrategy: Check if even N can be split into two primes.\nSample Input: 28\nSample Output: True", "Actual Input: 11", "False"),
        ("Problem 17: Euler Totient phi(N)\nConcept: Coprimality count.\nStrategy: Iterate through prime factors p; result = result * (1 - 1/p).\nSample Input: 9\nSample Output: 6", "Actual Input: 10", "4"),
        ("Problem 18: Catalan Numbers\nConcept: Combinatorial paths.\nStrategy: Use the formula C(n) = (2n)! / ((n+1)!n!).\nSample Input: 3\nSample Output: 5", "Actual Input: 5", "42"),
        ("Problem 19: Primitive Root\nConcept: Cyclic groups in math.\nStrategy: Find the smallest 'g' where g^i mod P generates all values.\nSample Input: 7\nSample Output: 3", "Actual Input: 13", "2"),
        ("Problem 20: Ugly Number\nConcept: Prime factor restriction.\nStrategy: Divide by 2, 3, and 5 until 1 is reached.\nSample Input: 6\nSample Output: True", "Actual Input: 14", "False"),
        ("Problem 21: Pascal Row Sum\nConcept: Binomial coefficients.\nStrategy: The sum of the Nth row is 2^(N-1).\nSample Input: 4\nSample Output: 8", "Actual Input: 10", "512"),
        ("Problem 22: String Digital Root\nConcept: Large number reductions.\nStrategy: Map (Sum of digits % 9); if 0, result is 9.\nSample Input: '9875'\nSample Output: 2", "Actual Input: '123456'", "3"),
        ("Problem 23: Largest Prime Factor\nConcept: Optimized prime hunting.\nStrategy: Divide by 2, then odd numbers until sqrt(N).\nSample Input: 13195\nSample Output: 29", "Actual Input: 84", "7"),
        ("Problem 24: Prime Count below N\nConcept: Prime Sieve efficiency.\nStrategy: Implement Sieve of Eratosthenes.\nSample Input: 10\nSample Output: 4", "Actual Input: 50", "15"),
        ("Problem 25: Hamming Distance\nConcept: Bitwise differences.\nStrategy: XOR the numbers and count set bits.\nSample Input: 1, 4\nSample Output: 2", "Actual Input: 15, 30", "1"),
        ("Problem 26: Swap Bits\nConcept: Binary manipulation.\nStrategy: Extract even/odd bits using masks 0xAAAAAAAA and 0x55555555.\nSample Input: 23\nSample Output: 43", "Actual Input: 10", "5"),
        ("Problem 27: Nth Prime\nConcept: Prime generation.\nStrategy: Incrementally check odd numbers until the count reaches N.\nSample Input: 5\nSample Output: 11", "Actual Input: 10", "29"),
        ("Problem 28: Smallest Multiple (LCM 1..N)\nConcept: Multiple LCM logic.\nStrategy: LCM(a, b) = (a*b)/GCD(a,b).\nSample Input: 5\nSample Output: 60", "Actual Input: 10", "2520"),
        ("Problem 29: Pronic Number\nConcept: Sequential multiplication.\nStrategy: Check if sqrt(N) * (sqrt(N)+1) == N.\nSample Input: 110\nSample Output: True", "Actual Input: 272", "True"),
        ("Problem 30: XOR Sum 1..N\nConcept: Cyclic XOR patterns.\nStrategy: Use the property that XOR sum repeats every 4 numbers.\nSample Input: 4\nSample Output: 4", "Actual Input: 10", "11"),

        # --- PHASE 2: ARRAYS & MATRICES (DAYS 31-60) ---
        ("Problem 31: Array Rotation\nConcept: Cyclic shifts.\nStrategy: Reverse portions of the array to achieve O(1) space.\nSample Input: [1,2], 1\nSample Output: [2,1]", "Actual Input: [1,2,3,4,5], 2", "[4,5,1,2,3]"),
        ("Problem 32: Kadane’s Algorithm\nConcept: Maximum sum subarray.\nStrategy: Track current_sum and max_sum in a single pass.\nSample Input: [-1, 2, 3]\nSample Output: 5", "Actual Input: [-2, 1, -3, 4, -1, 2]", "4"),
        ("Problem 33: Matrix Rotate 90\nConcept: Coordinate transformation.\nStrategy: Transpose the matrix, then reverse each row.\nSample Input: [[1,2],[3,4]]\nSample Output: [[3,1],[4,2]]", "Actual Input: [[1,0],[0,0]]", "[[0,1],[0,0]]"),
        ("Problem 34: Spiral Traversal\nConcept: Boundary shrinking logic.\nStrategy: Track top, bottom, left, and right indices.\nSample Input: [[1,2],[3,4]]\nSample Output: [1,2,4,3]", "Actual Input: [[1,2,3],[4,5,6],[7,8,9]]", "[1,2,3,6,9,8,7,4,5]"),
        ("Problem 35: First Unique Char\nConcept: Frequency mapping.\nStrategy: Count occurrences and return the first char with count 1.\nSample Input: 'swiss'\nSample Output: 'w'", "Actual Input: 'racecar'", "'e'"),
        ("Problem 36: Longest Substring\nConcept: Sliding window technique.\nStrategy: Use a pointer and a hash map of last seen indices.\nSample Input: 'abcabc'\nSample Output: 3", "Actual Input: 'bbbbb'", "1"),
        ("Problem 37: Anagram Check\nConcept: String sorting or counting.\nStrategy: Compare sorted versions or frequency maps.\nSample Input: 'art', 'rat'\nSample Output: True", "Actual Input: 'hello', 'world'", "False"),
        ("Problem 38: Array Intersection\nConcept: Set theory.\nStrategy: Use hash sets to find common elements.\nSample Input: [1,2], [2,3]\nSample Output: [2]", "Actual Input: [4,9,5], [9,4]", "[9,4]"),
        ("Problem 39: Rain Water Trapping\nConcept: Elevation analysis.\nStrategy: Find max_left and max_right for each point.\nSample Input: [0,1,0,2]\nSample Output: 1", "Actual Input: [3,0,2,0,4]", "7"),
        ("Problem 40: Missing Number\nConcept: Arithmetic series sum.\nStrategy: Subtract array sum from expected total sum.\nSample Input: [3,0,1]\nSample Output: 2", "Actual Input: [0,1]", "2"),
        ("Problem 41: Matrix Transpose\nConcept: Swap indices.\nStrategy: New_matrix[j][i] = old_matrix[i][j].\nSample Input: [[1,2],[3,4]]\nSample Output: [[1,3],[2,4]]", "Actual Input: [[1,2]]", "[[1],[2]]"),
        ("Problem 42: Product Except Self\nConcept: Prefix and Suffix arrays.\nStrategy: Multiple prefix products by suffix products.\nSample Input: [1,2,3]\nSample Output: [6,3,2]", "Actual Input: [4,5,2]", "[10,8,20]"),
        ("Problem 43: Second Largest\nConcept: Tournament logic.\nStrategy: Track 'max' and 'second_max' in one pass.\nSample Input: [1,2,3]\nSample Output: 2", "Actual Input: [10,10,9]", "9"),
        ("Problem 44: Common Prefix\nConcept: Horizontal scanning.\nStrategy: Compare chars of all strings at index i.\nSample Input: ['flow','fly']\nSample Output: 'fl'", "Actual Input: ['dog','car']", "''"),
        ("Problem 45: Equal Sum Partition\nConcept: Binary Subset Sum.\nStrategy: Check if total_sum/2 is reachable via DP.\nSample Input: [1,5,11,5]\nSample Output: True", "Actual Input: [1,2,3,5]", "False"),
        ("Problem 46: Reverse Words\nConcept: String tokenization.\nStrategy: Split by space, reverse the list, and join.\nSample Input: 'sky blue'\nSample Output: 'blue sky'", "Actual Input: 'hi me'", "'me hi'"),
        ("Problem 47: String Compression\nConcept: Run-length encoding.\nStrategy: Traverse and append char + count to a result.\nSample Input: 'aaab'\nSample Output: 'a3b1'", "Actual Input: 'aabbcc'", "'a2b2c2'"),
        ("Problem 48: Move Zeros\nConcept: Two-pointer swap.\nStrategy: Pointer 'i' finds non-zeros, 'j' tracks position.\nSample Input: [0,1,0,3]\nSample Output: [1,3,0,0]", "Actual Input: [0,0,1]", "[1,0,0]"),
        ("Problem 49: Majority Element\nConcept: Boyer-Moore Voting Algorithm.\nStrategy: Maintain a candidate and a counter.\nSample Input: [3,2,3]\nSample Output: 3", "Actual Input: [1,1,2]", "1"),
        ("Problem 50: Median Sorted Arrays\nConcept: Binary Search on partitions.\nStrategy: Partition arrays to balance left and right halves.\nSample Input: [1,3], [2]\nSample Output: 2.0", "Actual Input: [1,2], [3,4]", "2.5"),
        ("Problem 51: Edit Distance\nConcept: Levenshtein distance.\nStrategy: Use DP to calculate min (insert, delete, replace).\nSample Input: 'horse','ros'\nSample Output: 3", "Actual Input: 'abc','ybc'", "1"),
        ("Problem 52: Longest Palindrome\nConcept: Expand around center.\nStrategy: Check odd/even length palindromes for each index.\nSample Input: 'babad'\nSample Output: 'bab'", "Actual Input: 'cbbd'", "'bb'"),
        ("Problem 53: 2D Matrix Search\nConcept: Staircase search.\nStrategy: Start from top-right corner; move left or down.\nSample Input: [[1,3],[10,11]], 3\nSample Output: True", "Actual Input: [[1,2]], 3", "False"),
        ("Problem 54: Most Water\nConcept: Two-pointer shrink.\nStrategy: Move pointer at the shorter height inward.\nSample Input: [1,8,6,2]\nSample Output: 6", "Actual Input: [1,1]", "1"),
        ("Problem 55: All Subsets\nConcept: Power set recursion.\nStrategy: Use backtracking or bitmasking.\nSample Input: [1,2]\nSample Output: [[],[1],[2],[1,2]]", "Actual Input: [1]", "[[],[1]]"),
        ("Problem 56: Pascal Triangle Row\nConcept: Combinations property.\nStrategy: Use C(n, i) = C(n, i-1) * (n-i+1)/i.\nSample Input: 3\nSample Output: [1,3,3,1]", "Actual Input: 2", "[1,2,1]"),
        ("Problem 57: Sudoku Block Check\nConcept: Subgrid validation.\nStrategy: Use sets to check for duplicates in 3x3 grids.\nSample Input: matrix\nSample Output: True", "Actual Input: [[5,3,4],[6,7,2],[1,9,8]]", "True"),
        ("Problem 58: Find All Anagrams\nConcept: Sliding window frequencies.\nStrategy: Compare window frequency map with target map.\nSample Input: 'abab', 'ab'\nSample Output: [0, 1, 2]", "Actual Input: 'pwwk', 'wk'", "[2]"),
        ("Problem 59: Sort Colors\nConcept: Dutch National Flag.\nStrategy: Three pointers: low, mid, and high.\nSample Input: [2,0,1]\nSample Output: [0,1,2]", "Actual Input: [1,0]", "[0,1]"),
        ("Problem 60: Peak Element\nConcept: Binary Search on slopes.\nStrategy: Move towards the side with a greater neighbor.\nSample Input: [1,2,3,1]\nSample Output: 2", "Actual Input: [1,2,1]", "1"),

        # --- PHASE 3: ADVANCED DP, GRAPHS & COMPILER LOGIC (DAYS 61-90) ---
        ("Problem 61: N-Queens\nConcept: Backtracking constraint satisfaction.\nStrategy: Place queens row-by-row; check diagonals/cols.\nSample Input: 4\nSample Output: 2", "Actual Input: 1", "1"),
        ("Problem 62: KMP Algorithm\nConcept: String preprocessing.\nStrategy: Create a Longest Prefix Suffix (LPS) array.\nSample Input: 'abcx','bc'\nSample Output: 1", "Actual Input: 'aaaa','aa'", "0"),
        ("Problem 63: Wildcard Match\nConcept: 2D Pattern matching.\nStrategy: Use DP; '*' matches sequence, '?' matches char.\nSample Input: 'aa','*'\nSample Output: True", "Actual Input: 'aa','a'", "False"),
        ("Problem 64: Min Coin Change\nConcept: Unbounded knapsack.\nStrategy: dp[i] = min(dp[i], dp[i-coin] + 1).\nSample Input: [1,2,5], 11\nSample Output: 3", "Actual Input: [2], 3", "-1"),
        ("Problem 65: Word Break\nConcept: String segmentation.\nStrategy: Check if dp[j] is True and s[j:i] is in dict.\nSample Input: 'code',['co','de']\nSample Output: True", "Actual Input: 'abc',['a']", "False"),
        ("Problem 66: Kth Permutation\nConcept: Factorial number system.\nStrategy: Use factorials to skip blocks of permutations.\nSample Input: 3, 3\nSample Output: '213'", "Actual Input: 3, 1", "'123'"),
        ("Problem 67: Longest Increasing Subsequence\nConcept: Patience sorting logic.\nStrategy: Use binary search to maintain tails of subsequences.\nSample Input: [10,9,2,5]\nSample Output: 2", "Actual Input: [1,2,3]", "3"),
        ("Problem 68: Shortest Binary Path\nConcept: Breadth-First Search (BFS).\nStrategy: Traverse neighbors level by level.\nSample Input: [[0,0],[0,0]]\nSample Output: 2", "Actual Input: [[0,1],[1,0]]", "-1"),
        ("Problem 69: Sliding Window Max\nConcept: Monotonic Deque.\nStrategy: Keep indices of max elements in a deque.\nSample Input: [1,3,-1], 2\nSample Output: [3,3]", "Actual Input: [1,2,3], 1", "[1,2,3]"),
        ("Problem 70: Gas Station Circuit\nConcept: Greedy accumulation.\nStrategy: Check if total_gas >= total_cost; track surplus.\nSample Input: gas=[1], cost=[1]\nSample Output: 0", "Actual Input: gas=[1], cost=[2]", "-1"),
        ("Problem 71: Max Product Subarray\nConcept: Sign reversal tracking.\nStrategy: Store min_prod and max_prod for each index.\nSample Input: [2,3,-2]\nSample Output: 6", "Actual Input: [-1,-2]", "2"),
        ("Problem 72: Generate Parentheses\nConcept: Catalan recursion.\nStrategy: Only add ')' if count of ')' < count of '('.\nSample Input: 2\nSample Output: ['(())','()()']", "Actual Input: 1", "['()']"),
        ("Problem 73: x+y+z=N Solutions\nConcept: Stars and Bars theorem.\nStrategy: Calculation is (N+r-1)C(r-1).\nSample Input: 3\nSample Output: 10", "Actual Input: 2", "6"),
        ("Problem 74: Egg Dropping (2 eggs)\nConcept: Minimax optimization.\nStrategy: Solve for floors = (x * (x+1))/2.\nSample Input: 10\nSample Output: 4", "Actual Input: 100", "14"),
        ("Problem 75: Matrix Rank\nConcept: Row Echelon Form.\nStrategy: Perform Gaussian elimination to count pivot rows.\nSample Input: [[1,0],[0,1]]\nSample Output: 2", "Actual Input: [[1,1],[1,1]]", "1"),
        ("Problem 76: Jump Game\nConcept: Greedy reachability.\nStrategy: Track furthest reachable index at each step.\nSample Input: [2,3,1]\nSample Output: True", "Actual Input: [3,2,1,0,4]", "False"),
        ("Problem 77: Climbing Stairs\nConcept: Fibonacci mapping.\nStrategy: Ways(n) = Ways(n-1) + Ways(n-2).\nSample Input: 3\nSample Output: 3", "Actual Input: 4", "5"),
        ("Problem 78: House Robber\nConcept: Non-adjacent maximization.\nStrategy: dp[i] = max(dp[i-1], dp[i-2] + current).\nSample Input: [1,2,3,1]\nSample Output: 4", "Actual Input: [1,1,1]", "2"),
        ("Problem 79: Next Permutation\nConcept: Lexicographical order.\nStrategy: Find pivot, swap with next successor, reverse tail.\nSample Input: [1,2,3]\nSample Output: [1,3,2]", "Actual Input: [3,2,1]", "[1,2,3]"),
        ("Problem 80: Clock Angle\nConcept: Angular velocity.\nStrategy: Angle = |30h - 5.5m|.\nSample Input: '12:00'\nSample Output: 0", "Actual Input: '3:00'", "90"),
        ("Problem 81: Course Schedule\nConcept: Topological Sorting.\nStrategy: Check for cycles using DFS or In-degree count.\nSample Input: 2, [[1,0],[0,1]]\nSample Output: False", "Actual Input: 2, [[1,0]]", "True"),
        ("Problem 82: Shortest Palindrome\nConcept: String mirroring.\nStrategy: Use KMP to find the longest palindrome prefix.\nSample Input: 'aace'\nSample Output: 'ecaaace'", "Actual Input: 'abc'", "'cbabc'"),
        ("Problem 83: Number of Islands\nConcept: Connected Components.\nStrategy: Use DFS to mark visited land cells.\nSample Input: [[1,1,0],[0,0,1]]\nSample Output: 2", "Actual Input: [[1,0],[0,1]]", "2"),
        ("Problem 84: Decode Ways\nConcept: Branching DP.\nStrategy: Check if s[i] and s[i-1:i+1] are valid codes.\nSample Input: '12'\nSample Output: 2", "Actual Input: '10'", "1"),
        ("Problem 85: Longest Common Subsequence\nConcept: 2D Alignment.\nStrategy: If chars match, 1 + dp[i-1][j-1]; else max(top, left).\nSample Input: 'abc','ace'\nSample Output: 2", "Actual Input: 'x','y'", "0"),
        ("Problem 86: Best Stock Profit\nConcept: Greedy pass.\nStrategy: Track min_price and max_profit seen so far.\nSample Input: [7,1,5]\nSample Output: 4", "Actual Input: [7,6,5]", "0"),
        ("Problem 87: Palindrome Partitioning\nConcept: Min Cuts DP.\nStrategy: dp[i] is min cuts for s[0:i].\nSample Input: 'aab'\nSample Output: 1", "Actual Input: 'aba'", "0"),
        ("Problem 88: Median Data Stream\nConcept: Dual Heap structure.\nStrategy: Use a max-heap (left) and min-heap (right).\nSample Input: [1, 2, 3]\nSample Output: 2", "Actual Input: [10, 20]", "15.0"),
        ("Problem 89: Rotated Array Search\nConcept: Modified binary search.\nStrategy: Determine which half (left/right) is sorted.\nSample Input: [4,5,6,0,1,2], 0\nSample Output: 3", "Actual Input: [1], 0", "-1"),
        ("Problem 90: Regex Engine\nConcept: NFA Simulation.\nStrategy: Use DP to handle '.' and '*' patterns.\nSample Input: 'aa','a*'\nSample Output: True", "Actual Input: 'ab','.*'", "True"),
    ]

    start_date = datetime(2025, 12, 24)
    final_questions = []

    for i in range(len(challenges)):
        current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        logic_brief, actual_input, expected_answer = challenges[i]
        
        # Extract the Title (e.g., "Problem 1: Mixed Power Series")
        title = logic_brief.split('\n')[0]
        
        # Format for front-end clarity
        full_content = f"{logic_brief}\n\n{actual_input}"
        
        # Added 'title' to the tuple to match the new DB schema
        final_questions.append((title, current_date, full_content, "", expected_answer))

    # Execute insertion using %s placeholders for PostgreSQL
    cursor.executemany("""
        INSERT INTO questions (title, date, content, solution, expected_output)
        VALUES (%s, %s, %s, %s, %s)
    """, final_questions)

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Supabase updated with exactly {len(challenges)} unique professional problems.")

if __name__ == "__main__":
    setup_curriculum()