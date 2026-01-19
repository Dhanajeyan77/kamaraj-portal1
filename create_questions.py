import os
import psycopg2
from datetime import datetime, timedelta

def setup_professional_curriculum():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ ERROR: DATABASE_URL is not set.")
        return

    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Clean table before insertion (optional but intentional)
        cursor.execute("DELETE FROM questions")

        # ======================================================
        # 🔴 ONLY MANUAL CONTENT — NO AUTO GENERATION
        # Add ALL 90 problems here (deep Gemini content)
        # ======================================================
        challenges = [

            # 1. PALINDROME NUMBER
            (
                "Problem 1: Palindrome Number",
                "### Problem Overview\nDetermine if an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.\n\n"
                "### Core Concept\nNumeric reversal and digit extraction without string conversion.\n\n"
                "### Detailed Logic\n1. Eliminate negative numbers immediately.\n2. Extract digits using `n % 10`.\n3. Build the reversed number: `rev = (rev * 10) + digit`.\n4. Compare reversed result to original.\n\n"
                "### Edge Case Notes\n- Negative numbers are not palindromes.\n- Numbers ending in 0 (except 0 itself) are not palindromes.\n\n"
                "### Example Walkthrough\n**Input:** 121 -> Reversed: 121. **Match: True**"
            ),

            # 2. PERFECT NUMBER
            (
                "Problem 2: Perfect Number",
                "### Problem Overview\nA perfect number is a positive integer equal to the sum of its proper divisors (excluding itself).\n\n"
                "### Core Concept\nEfficient divisor hunting and summation logic.\n\n"
                "### Detailed Logic\n1. Iterate from 1 up to the square root of N.\n2. If `i` divides N, add `i` and `N/i` to the sum.\n3. Be careful not to add the number itself.\n\n"
                "### Edge Case Notes\n- 1 is not a perfect number.\n\n"
                "### Example Walkthrough\n**Input:** 6 -> Divisors (1,2,3). Sum = 6. **Match: True**"
            ),
            # 3. ARMSTRONG NUMBER
            (
                "Problem 3: Armstrong Number",
                "### Problem Overview\nCheck if a number equals the sum of its digits raised to the power of the count of digits.\n\n"
                "### Core Concept\nDigit separation and exponential summation.\n\n"
                "### Detailed Logic\n1. Calculate the number of digits (k).\n2. Extract each digit, raise it to the power of k.\n3. Sum these values and compare to original.\n\n"
                "### Edge Case Notes\n- All single-digit numbers are Armstrong numbers.\n\n"
                "### Example Walkthrough\n**Input:** 153 -> (1³ + 5³ + 3³) = 153. **Match: True**"
            ),
            # 4. PRIME NUMBER
            (
                "Problem 4: Prime Number Check",
                "### Problem Overview\nDetermine if a number has exactly two divisors: 1 and itself.\n\n"
                "### Core Concept\nPrimality testing using the square root rule.\n\n"
                "### Detailed Logic\n1. If N <= 1, return False.\n2. Iterate from 2 to sqrt(N).\n3. If any number divides N, it is not prime.\n\n"
                "### Edge Case Notes\n- 2 is the only even prime.\n\n"
                "### Example Walkthrough\n**Input:** 7 -> No divisors between 2 and 2.6. **Match: True**"
            ),
            # 5. SIEVE OF ERATOSTHENES
            (
                "Problem 5: Sieve of Eratosthenes",
                "### Problem Overview\nFind all prime numbers up to a given limit N.\n\n"
                "### Core Concept\nEfficient elimination of multiples in an array.\n\n"
                "### Detailed Logic\n1. Create a boolean array of size N+1 initialized to True.\n2. Starting from 2, mark all its multiples as False.\n3. Move to the next True index and repeat.\n\n"
                "### Edge Case Notes\n- Optimal for finding many primes at once.\n\n"
                "### Example Walkthrough\n**Input:** 10 -> Primes: 2, 3, 5, 7."
            ),

            (
            "Problem 6: Factorial Logic",
            "### Problem Overview\nCalculate the product of all positive integers from 1 to N. Factorial (N!) represents the number of ways to arrange N distinct objects.\n\n"
            "### Core Concept\nSequential multiplication and recursion. This tests your understanding of iterative growth and base-case logic.\n\n"
            "### Detailed Logic\n1. If N is 0 or 1, return 1 (Base case: 0! and 1! are mathematically defined as 1).\n"
            "2. Initialize a result variable to 1.\n"
            "3. Loop from 2 up to N, multiplying the result by the current index at each step.\n"
            "4. Alternatively, use recursion: $Fact(N) = N * Fact(N-1)$.\n\n"
            "### Edge Case Notes\n- Negative numbers: Factorial is not defined for negative integers.\n- Overflow: Factorial grows extremely fast; use 64-bit integers for N > 12.\n\n"
            "### Example Walkthrough\n**Input:** 5\n- 1 * 2 = 2\n- 2 * 3 = 6\n- 6 * 4 = 24\n- 24 * 5 = 120\n**Result: 120**"
        ),
        (
            "Problem 7: Fibonacci Nth Term",
            "### Problem Overview\nFind the Nth number in the Fibonacci sequence, where each number is the sum of the two preceding ones, starting from 0 and 1.\n\n"
            "### Core Concept\nState tracking and Dynamic Programming. This tests how you manage multiple variables that evolve over time.\n\n"
            "### Detailed Logic\n1. Handle base cases: If N=0, return 0. If N=1, return 1.\n"
            "2. Initialize two variables: `prev = 0` and `curr = 1`.\n"
            "3. Iterate from 2 to N.\n"
            "4. Calculate `next = prev + curr`.\n"
            "5. Update: `prev = curr` and `curr = next`.\n"
            "6. After the loop, `curr` holds the Nth value.\n\n"
            "### Edge Case Notes\n- Time Complexity: The iterative approach is $O(N)$, whereas basic recursion is $O(2^N)$.\n\n"
            "### Example Walkthrough\n**Input:** N = 4\n- Step 1 (index 2): 0 + 1 = 1\n- Step 2 (index 3): 1 + 1 = 2\n- Step 3 (index 4): 1 + 2 = 3\n**Result: 3**"
        ),
        (
            "Problem 8: Greatest Common Divisor (GCD)",
            "### Problem Overview\nFind the largest positive integer that divides two numbers without leaving a remainder.\n\n"
            "### Core Concept\nEuclidean Algorithm. Instead of checking every possible divisor, you use the remainder to shrink the problem size rapidly.\n\n"
            "### Detailed Logic\n1. While the second number (b) is not zero:\n"
            "2. Calculate the remainder of $a / b$ ($r = a \pmod b$).\n"
            "3. Update: $a = b$ and $b = r$.\n"
            "4. When $b$ becomes 0, the current value of $a$ is the GCD.\n\n"
            "### Edge Case Notes\n- If one number is 0, the GCD is the other number.\n\n"
            "### Example Walkthrough\n**Input:** a=48, b=18\n- 48 % 18 = 12 -> (18, 12)\n- 18 % 12 = 6 -> (12, 6)\n- 12 % 6 = 0 -> (6, 0)\n**Result: 6**"
        ),
        (
            "Problem 9: Least Common Multiple (LCM)",
            "### Problem Overview\nFind the smallest positive integer that is a multiple of two given numbers.\n\n"
            "### Core Concept\nFundamental Theorem of Arithmetic. The relationship between GCD and LCM is: $LCM(a, b) = \frac{|a \times b|}{GCD(a, b)}$.\n\n"
            "### Detailed Logic\n1. Calculate the GCD of the two numbers using the Euclidean Algorithm.\n"
            "2. Multiply the two numbers (a * b).\n"
            "3. Divide the product by the GCD.\n"
            "4. Perform division before multiplication if numbers are large to prevent overflow.\n\n"
            "### Edge Case Notes\n- If either number is 0, the LCM is 0.\n\n"
            "### Example Walkthrough\n**Input:** a=12, b=15\n- GCD(12, 15) is 3.\n- (12 * 15) / 3 = 180 / 3 = 60.\n**Result: 60**"
        ),
        (
            "Problem 10: Binary to Decimal",
            "### Problem Overview\nConvert a binary number (base-2, represented as a string or integer) into its decimal (base-10) equivalent.\n\n"
            "### Core Concept\nPositional Notation. Each digit represents a power of 2, starting from $2^0$ on the far right.\n\n"
            "### Detailed Logic\n1. Initialize `decimal = 0` and `power = 0`.\n"
            "2. Iterate through the binary digits from right to left.\n"
            "3. If the digit is 1, add $2^{power}$ to the `decimal` sum.\n"
            "4. Increment `power` for every digit processed.\n\n"
            "### Edge Case Notes\n- Binary strings can be long; ensure the resulting decimal can fit in a 64-bit integer.\n\n"
            "### Example Walkthrough\n**Input:** 1011\n- (1 * 2^0) = 1\n- (1 * 2^1) = 2\n- (0 * 2^2) = 0\n- (1 * 2^3) = 8\n**Total: 1+2+0+8 = 11**"
        ),
        (
            "Problem 11: Decimal to Binary",
            "### Problem Overview\nConvert a decimal integer (base-10) into its binary string (base-2) representation.\n\n"
            "### Core Concept\nSuccessive Division. Dividing by 2 repeatedly extracts bits from the least significant to the most significant.\n\n"
            "### Detailed Logic\n1. If the number is 0, return '0'.\n"
            "2. While the number is greater than 0:\n"
            "3. Find the remainder when divided by 2 (this is the bit).\n"
            "4. Append the bit to a collection (or string).\n"
            "5. Update the number by dividing it by 2 (integer division).\n"
            "6. Reverse the collection/string to get the final binary order.\n\n"
            "### Edge Case Notes\n- Negative numbers usually require 'Two's Complement' representation (standard conversion often assumes unsigned).\n\n"
            "### Example Walkthrough\n**Input:** 13\n- 13/2 = 6, rem 1\n- 6/2 = 3, rem 0\n- 3/2 = 1, rem 1\n- 1/2 = 0, rem 1\n**Reverse '1011' to get 1101**"
        ),
        (
            "Problem 12: Strong Number",
            "### Problem Overview\nA Strong Number is a special number whose sum of the factorial of its digits is equal to the number itself.\n\n"
            "### Core Concept\nDigit Decomposition. This requires extracting digits and applying a sub-function (Factorial) to each.\n\n"
            "### Detailed Logic\n1. Store the original number in a temporary variable.\n"
            "2. Initialize `total_sum = 0`.\n"
            "3. While number > 0:\n"
            "4. Extract the last digit using `% 10`.\n"
            "5. Calculate the factorial of that digit.\n"
            "6. Add the factorial to `total_sum`.\n"
            "7. Compare `total_sum` with the original number.\n\n"
            "### Edge Case Notes\n- Pre-calculating factorials of 0-9 in an array can significantly speed up the process.\n\n"
            "### Example Walkthrough\n**Input:** 145\n- 1! = 1\n- 4! = 24\n- 5! = 120\n- 1 + 24 + 120 = 145. **Match: True**"
        ),
        (
            "Problem 13: Reverse an Integer",
            "### Problem Overview\nGiven a signed 32-bit integer, return the integer with its digits reversed.\n\n"
            "### Core Concept\nMathematical digit shifting. Avoid string conversion to demonstrate numeric proficiency.\n\n"
            "### Detailed Logic\n1. Initialize `reversed_num = 0`.\n"
            "2. While the input number is not zero:\n"
            "3. Pop the last digit: `pop = num % 10`.\n"
            "4. Before updating, check if multiplying `reversed_num` by 10 will cause overflow.\n"
            "5. Push the digit: `reversed_num = (reversed_num * 10) + pop`.\n"
            "6. Update the number: `num = num / 10`.\n\n"
            "### Edge Case Notes\n- Negative signs: In many languages, `-123 % 10` is `-3`. Ensure the sign is handled correctly.\n\n"
            "### Example Walkthrough\n**Input:** -123\n- Pop -3: reversed = -3\n- Pop -2: reversed = -32\n- Pop -1: reversed = -321\n**Result: -321**"
        ),
        (
            "Problem 14: Leap Year Logic",
            "### Problem Overview\nDetermine whether a given year is a leap year in the Gregorian calendar.\n\n"
            "### Core Concept\nConditional Branching. This tests your ability to translate complex business rules into nested or compound logic.\n\n"
            "### Detailed Logic\n1. A year is a leap year if it is divisible by 4.\n"
            "2. EXCEPT if it is divisible by 100, it is NOT a leap year.\n"
            "3. UNLESS it is also divisible by 400, in which case it IS a leap year.\n"
            "4. Formula: `(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)`.\n\n"
            "### Edge Case Notes\n- Year 2000 was a leap year (divisible by 400).\n- Year 1900 was not a leap year (divisible by 100 but not 400).\n\n"
            "### Example Walkthrough\n**Input:** 1900\n- Divisible by 4? Yes.\n- Divisible by 100? Yes.\n- Divisible by 400? No.\n**Result: False**"
        ),
        (
            "Problem 15: Pascal's Triangle Value",
            "### Problem Overview\nGiven a row and a column index, find the specific value at that position in Pascal's Triangle.\n\n"
            "### Core Concept\nCombinatorics. The value at Row $n$, Column $k$ is given by the binomial coefficient $\binom{n}{k}$.\n\n"
            "### Detailed Logic\n1. Use the formula: $\binom{n}{k} = \frac{n!}{k!(n-k)!}$.\n"
            "2. To be more efficient and avoid large factorials, use the iterative multiplicative formula:\n"
            "3. Result = 1. For $i$ from 0 to $k-1$:\n"
            "4. Result = Result * $(n - i) / (i + 1)$.\n\n"
            "### Edge Case Notes\n- Column index $k$ cannot be greater than row index $n$.\n- Positions at the edges (column 0 or column $n$) are always 1.\n\n"
            "### Example Walkthrough\n**Input:** Row 4, Col 2\n- Pascal Row 4 is: 1, 4, 6, 4, 1\n- Index 2 is 6.\n**Result: 6**"
        ),

        (
            "Problem 16: Reverse a String",
            "### Problem Overview\nModify a string so that the character sequence is inverted (the last character becomes the first, the second-to-last becomes the second, and so on).\n\n"
            "### Core Concept\nTwo-Pointer Technique. This is the foundation of in-place array manipulation, ensuring minimal memory usage ($O(1)$ extra space).\n\n"
            "### Detailed Logic\n1. Initialize a `left` pointer at index 0 and a `right` pointer at `length - 1`.\n"
            "2. While `left < right`, swap the characters at these two positions.\n"
            "3. Increment `left` and decrement `right`.\n"
            "4. **Note:** In languages where strings are immutable (like Java/Python), you must first convert the string to a character array or use a builder.\n\n"
            "### Edge Case Notes\n- Single character strings: No swap occurs.\n- Empty strings: Handled by the `while` condition immediately.\n\n"
            "### Example Walkthrough\n**Input:** 'code'\n1. Swap 'c' and 'e' -> 'eodc'\n2. Swap 'o' and 'd' -> 'edoc'\n**Result: 'edoc'**"
        ),
        (
            "Problem 17: Check Anagrams",
            "### Problem Overview\nTwo strings are anagrams if they contain the exact same characters with the same frequencies, rearranged in a different order.\n\n"
            "### Core Concept\nFrequency Distribution Mapping. This tests your ability to use Hash Maps or fixed-size arrays to count occurrences efficiently.\n\n"
            "### Detailed Logic\n1. If lengths are different, they cannot be anagrams; return False.\n"
            "2. Create a frequency array of size 26 (for 'a'-'z') or a Hash Map.\n"
            "3. Iterate through string A: increment the count for each character.\n"
            "4. Iterate through string B: decrement the count for each character.\n"
            "5. If every index in your frequency tracker is 0, the strings are anagrams.\n\n"
            "### Edge Case Notes\n- Case sensitivity: Typically convert to lowercase first.\n- Non-alphabetic characters: Decide if spaces and symbols should be ignored.\n\n"
            "### Example Walkthrough\n**Input:** 'silent', 'listen'\n- Both contain: {s:1, i:1, l:1, e:1, n:1, t:1}\n**Result: True**"
        ),
        (
            "Problem 18: Count Vowels and Consonants",
            "### Problem Overview\nAnalyze a string to determine how many characters are vowels (a, e, i, o, u) and how many are consonants.\n\n"
            "### Core Concept\nCharacter Classification. This tests basic iteration and set-membership logic.\n\n"
            "### Detailed Logic\n1. Initialize counters: `vowels = 0`, `consonants = 0`.\n"
            "2. Convert the string to lowercase.\n"
            "3. Iterate through each character: check if it is a letter.\n"
            "4. If it's a letter, check if it exists in the set {'a', 'e', 'i', 'o', 'u'}.\n"
            "5. Increment the appropriate counter.\n\n"
            "### Edge Case Notes\n- Ignore numbers, spaces, and punctuation.\n- Handle empty strings (both counts remain 0).\n\n"
            "### Example Walkthrough\n**Input:** 'Hello!'\n- h(C), e(V), l(C), l(C), o(V)\n- ! (Ignore)\n**Result: Vowels: 2, Consonants: 3**"
        ),
        (
            "Problem 19: First Non-Repeating Character",
            "### Problem Overview\nIdentify the first character in a string that appears exactly once.\n\n"
            "### Core Concept\nTwo-Pass Hashing. This demonstrates how to pre-process data into a summary (frequency map) before making a decision.\n\n"
            "### Detailed Logic\n1. **Pass 1:** Iterate through the string and build a frequency map of all characters.\n"
            "2. **Pass 2:** Iterate through the string a second time.\n"
            "3. For the current character, look up its frequency in the map.\n"
            "4. The first character you encounter with a frequency of 1 is the result.\n\n"
            "### Edge Case Notes\n- If no unique character exists, return a designated value like '_' or -1.\n\n"
            "### Example Walkthrough\n**Input:** 'swiss'\n- Map: {s:3, w:1, i:1}\n- Pass 2: 's'(3), 'w'(1) -> STOP.\n**Result: 'w'**"
        ),
        (
            "Problem 20: String Compression",
            "### Problem Overview\nCompress a string by replacing consecutive identical characters with the character followed by the count (e.g., 'aaabb' -> 'a3b2').\n\n"
            "### Core Concept\nRun-Length Encoding (RLE). This tests your ability to track a 'current character' and a 'counter' during a single pass.\n\n"
            "### Detailed Logic\n1. Initialize an empty result string/builder.\n"
            "2. Iterate through the string using a pointer `i`.\n"
            "3. While the character at `i` is the same as the character at `i + 1`, increment a counter.\n"
            "4. Append the character and the counter to the result.\n"
            "5. If the compressed string is not shorter than the original, standard practice is to return the original.\n\n"
            "### Edge Case Notes\n- Single character runs: 'a' becomes 'a1'.\n- Watch for 'Index Out of Bounds' when checking the next character.\n\n"
            "### Example Walkthrough\n**Input:** 'aaabbc'\n- a(3), b(2), c(1)\n**Result: 'a3b2c1'**"
        ),
        (
            "Problem 21: Remove Duplicate Characters",
            "### Problem Overview\nRemove all duplicate characters from a string so that only the first occurrence of each character remains.\n\n"
            "### Core Concept\nSet-based Filtering. Using a 'Seen' set allows for $O(1)$ lookup time to decide if a character should be kept.\n\n"
            "### Detailed Logic\n1. Initialize an empty 'Seen' set and an empty result builder.\n"
            "2. Iterate through the string character by character.\n"
            "3. If the character is NOT in the 'Seen' set:\n"
            "4. Add it to the set and append it to the result.\n"
            "5. If it is already in the set, skip it.\n\n"
            "### Edge Case Notes\n- Maintains the original relative order of characters.\n\n"
            "### Example Walkthrough\n**Input:** 'programming'\n- Result starts: 'p', 'r', 'o', 'g'...\n- Second 'r' found in 'Seen' -> Skip.\n**Result: 'progamin'**"
        ),
        (
            "Problem 22: Longest Common Prefix",
            "### Problem Overview\nFind the longest string that is a prefix of all strings in an array.\n\n"
            "### Core Concept\nHorizontal Scanning. This tests your ability to compare multiple items simultaneously or iteratively.\n\n"
            "### Detailed Logic\n1. Assume the first string is the prefix.\n"
            "2. Compare this prefix with the second string.\n"
            "3. Shorten the prefix until it matches the start of the second string.\n"
            "4. Repeat this process with the remaining strings.\n"
            "5. If the prefix becomes an empty string, return \"\".\n\n"
            "### Edge Case Notes\n- If the array is empty, return \"\".\n- The prefix can never be longer than the shortest string.\n\n"
            "### Example Walkthrough\n**Input:** ['flower', 'flow', 'flight']\n- Prefix 'flower' vs 'flow' -> Prefix becomes 'flow'\n- Prefix 'flow' vs 'flight' -> Prefix becomes 'fl'\n**Result: 'fl'**"
        ),
        (
            "Problem 23: String Rotation Check",
            "### Problem Overview\nDetermine if one string is a rotation of another (e.g., 'waterbottle' is a rotation of 'erbottlewat').\n\n"
            "### Core Concept\nConcatenation Trick. This is a clever optimization that turns a complex rotation check into a simple substring search.\n\n"
            "### Detailed Logic\n1. If lengths are different, return False.\n"
            "2. Create a new string by concatenating string A with itself (`A + A`).\n"
            "3. Check if string B is a substring of this new string.\n"
            "4. If `B` exists within `A + A`, then `B` is a rotation of `A`.\n\n"
            "### Edge Case Notes\n- 'abc' and 'abc' are rotations (0 degrees).\n\n"
            "### Example Walkthrough\n**Input:** s1='abc', s2='bca'\n- s1 + s1 = 'abcabc'\n- Is 'bca' in 'abcabc'? Yes.\n**Result: True**"
        ),
        (
            "Problem 24: Valid Parentheses",
            "### Problem Overview\nGiven a string containing just '(', ')', '{', '}', '[' and ']', determine if the brackets are closed in the correct order.\n\n"
            "### Core Concept\nStack (Last-In-First-Out). Brackets must be closed in the reverse order they were opened.\n\n"
            "### Detailed Logic\n1. Initialize an empty Stack.\n"
            "2. Iterate through the string: if you see an opening bracket, push it onto the stack.\n"
            "3. If you see a closing bracket, check the stack.\n"
            "4. If the stack is empty or the top of the stack doesn't match the closing type, return False.\n"
            "5. After the loop, if the stack is empty, return True.\n\n"
            "### Edge Case Notes\n- String starting with a closing bracket (False).\n- Extra opening brackets left at the end (False).\n\n"
            "### Example Walkthrough\n**Input:** '([])'\n1. Push '(', Push '['\n2. Match ']' with top '[' -> Pop '['\n3. Match ')' with top '(' -> Pop '('\n**Result: True**"
        ),
        (
            "Problem 25: String to Integer (atoi)",
            "### Problem Overview\nImplement a function that converts a string to a 32-bit signed integer (similar to C/C++'s `atoi` function).\n\n"
            "### Core Concept\nState Management and Overflow. You must handle whitespace, signs (+/-), and non-digit characters carefully.\n\n"
            "### Detailed Logic\n1. Trim leading whitespace.\n"
            "2. Check for a sign (+ or -) and store it.\n"
            "3. Read digits one by one until a non-digit character is reached or the string ends.\n"
            "4. Convert characters to digits (`char - '0'`) and build the number: `total = total * 10 + digit`.\n"
            "5. Check for 32-bit integer overflow/underflow at each step.\n\n"
            "### Edge Case Notes\n- \"  -42\" -> -42.\n- \"4193 with words\" -> 4193.\n- String starts with letters -> 0.\n\n"
            "### Example Walkthrough\n**Input:** '   -42'\n- Trim -> '-42'\n- Sign detected -> Negative\n- 4, then 2 -> total = 42\n**Result: -42**"
        ),

        (
            "Problem 26: Reverse Words in a Sentence",
            "### Problem Overview\nGiven an input string, reverse the order of the words while keeping the characters within each word in the correct order.\n\n"
            "### Core Concept\nTokenization and Two-Pointer swap. This tests your ability to handle groups of data within a linear sequence.\n\n"
            "### Detailed Logic\n1. Trim leading and trailing spaces and split the string into words using whitespace as a delimiter.\n"
            "2. Use a two-pointer approach (start and end) to swap the words in the resulting list.\n"
            "3. Join the words back together with a single space.\n"
            "4. **Alternative:** Reverse the entire string character-by-character, then reverse the characters of each individual word.\n\n"
            "### Edge Case Notes\n- Multiple spaces between words should be reduced to a single space.\n\n"
            "### Example Walkthrough\n**Input:** 'sky is blue'\n1. Split -> ['sky', 'is', 'blue']\n2. Swap -> ['blue', 'is', 'sky']\n**Result: 'blue is sky'**"
        ),
        (
            "Problem 27: Find Max and Min in Array",
            "### Problem Overview\nFind both the maximum and the minimum element in an unsorted array in the fewest possible comparisons.\n\n"
            "### Core Concept\nLinear Scanning. This is a fundamental pattern for gathering global statistics from a local stream of data.\n\n"
            "### Detailed Logic\n1. Initialize `max` and `min` with the first element of the array.\n"
            "2. Iterate through the array starting from the second element.\n"
            "3. If the current element is greater than `max`, update `max`.\n"
            "4. Else if the current element is smaller than `min`, update `min`.\n"
            "5. To optimize: Process elements in pairs and compare the smaller of the pair to `min` and the larger to `max` (reduces total comparisons).\n\n"
            "### Edge Case Notes\n- Empty array: Decide on a return value (e.g., Error or Null).\n- Array with one element: Both Max and Min are the same.\n\n"
            "### Example Walkthrough\n**Input:** [3, 5, 1, 9]\n- Initialize: Max=3, Min=3\n- Compare 5: Max=5\n- Compare 1: Min=1\n- Compare 9: Max=9\n**Result: Max: 9, Min: 1**"
        ),
        (
            "Problem 28: Second Largest Element",
            "### Problem Overview\nFind the second largest distinct element in an array without sorting.\n\n"
            "### Core Concept\nSingle-Pass tracking. This tests your ability to maintain multiple levels of state simultaneously.\n\n"
            "### Detailed Logic\n1. Initialize two variables: `largest = -infinity` and `second_largest = -infinity`.\n"
            "2. Iterate through each number in the array.\n"
            "3. If `num > largest`:\n"
            "   - Update `second_largest = largest`\n"
            "   - Update `largest = num`\n"
            "4. Else if `num > second_largest` AND `num != largest`:\n"
            "   - Update `second_largest = num`.\n\n"
            "### Edge Case Notes\n- If the array has fewer than two distinct elements, the second largest may not exist.\n\n"
            "### Example Walkthrough\n**Input:** [10, 5, 10, 8]\n1. num=10: largest=10\n2. num=5: second=5\n3. num=10: (duplicate, skip)\n4. num=8: 8 > 5, so second=8.\n**Result: 8**"
        ),
        (
            "Problem 29: Move Zeros to End",
            "### Problem Overview\nGiven an array, move all 0s to the end while maintaining the relative order of the non-zero elements.\n\n"
            "### Core Concept\nIn-place Partitioning. This problem is similar to the 'Quicksort' partition logic, focusing on shifting elements without auxiliary space.\n\n"
            "### Detailed Logic\n1. Initialize a pointer `last_non_zero = 0`.\n"
            "2. Iterate through the array with a pointer `i`.\n"
            "3. If `arr[i]` is not zero, swap `arr[i]` with `arr[last_non_zero]` and increment `last_non_zero`.\n"
            "4. This effectively pushes non-zero elements to the front and zeros to the back.\n\n"
            "### Edge Case Notes\n- Array with no zeros.\n- Array with only zeros.\n\n"
            "### Example Walkthrough\n**Input:** [0, 1, 0, 3]\n1. i=1 (1): swap with index 0 -> [1, 0, 0, 3]\n2. i=3 (3): swap with index 1 -> [1, 3, 0, 0]\n**Result: [1, 3, 0, 0]**"
        ),
        (
            "Problem 30: Rotate Array (K Steps)",
            "### Problem Overview\nRotate an array to the right by `k` steps, where `k` is non-negative.\n\n"
            "### Core Concept\nReversal Algorithm. This is a highly efficient $O(N)$ time and $O(1)$ space solution to a problem that usually looks like it requires extra memory.\n\n"
            "### Detailed Logic\n1. Normalize `k` using `k = k % length` (to handle cases where k > length).\n"
            "2. Reverse the entire array.\n"
            "3. Reverse the first `k` elements.\n"
            "4. Reverse the remaining `length - k` elements.\n\n"
            "### Edge Case Notes\n- k = 0: No rotation needed.\n- k = length: No net change.\n\n"
            "### Example Walkthrough\n**Input:** [1, 2, 3, 4, 5], k=2\n1. Full Reverse: [5, 4, 3, 2, 1]\n2. Reverse first 2: [4, 5, 3, 2, 1]\n3. Reverse last 3: [4, 5, 1, 2, 3]\n**Result: [4, 5, 1, 2, 3]**"
        ),
        (
            "Problem 31: Find Missing Number",
            "### Problem Overview\nGiven an array containing $n$ distinct numbers in the range $[0, n]$, find the one number that is missing.\n\n"
            "### Core Concept\nArithmetic Sum Formula or XOR. This tests your ability to use mathematical properties to find anomalies.\n\n"
            "### Detailed Logic\n1. Calculate the expected sum of numbers from 0 to $n$ using the formula: $Sum = \frac{n(n+1)}{2}$.\n"
            "2. Calculate the actual sum of all elements in the array.\n"
            "3. The missing number is `Expected Sum - Actual Sum`.\n"
            "4. **Alternative:** XOR all indices from $0 \dots n$ and XOR all values in the array. The remaining value is the missing one.\n\n"
            "### Edge Case Notes\n- Missing 0 or missing $n$.\n\n"
            "### Example Walkthrough\n**Input:** [3, 0, 1] (n=3)\n- Expected: (3*4)/2 = 6\n- Actual: 3+0+1 = 4\n- Missing: 6 - 4 = 2.\n**Result: 2**"
        ),
        (
            "Problem 32: Intersection of Two Arrays",
            "### Problem Overview\nFind all unique elements that appear in both of two given arrays.\n\n"
            "### Core Concept\nSet-based Matching. This demonstrates how to use Hash Sets to achieve $O(N+M)$ time complexity instead of $O(N \times M)$.\n\n"
            "### Detailed Logic\n1. Insert all elements of the first array into a Hash Set (Set A).\n"
            "2. Create a second empty Hash Set (Result Set).\n"
            "3. Iterate through the second array; if an element exists in Set A, add it to the Result Set.\n"
            "4. Convert the Result Set back to an array.\n\n"
            "### Edge Case Notes\n- Arrays with no common elements.\n- Arrays with all identical elements.\n\n"
            "### Example Walkthrough\n**Input:** [1, 2, 2, 1], [2, 2]\n- Set A: {1, 2}\n- Check [2, 2]: 2 is in Set A. Result Set: {2}\n**Result: [2]**"
        ),
        (
            "Problem 33: Two Sum",
            "### Problem Overview\nFind two numbers in an array such that they add up to a specific target number. Return their indices.\n\n"
            "### Core Concept\nComplement Hashing. This is the ultimate 'trade memory for speed' pattern.\n\n"
            "### Detailed Logic\n1. Initialize an empty Hash Map: `{Value: Index}`.\n"
            "2. Iterate through the array.\n"
            "3. For each number, calculate `complement = target - current_value`.\n"
            "4. If the `complement` is already in the Hash Map, return the current index and the complement's index.\n"
            "5. Otherwise, add the current value and index to the Hash Map.\n\n"
            "### Edge Case Notes\n- Assumes exactly one solution exists.\n- You cannot use the same element twice.\n\n"
            "### Example Walkthrough\n**Input:** [2, 7, 11, 15], target=9\n- 2: complement 7 (not in map). Map: {2: 0}\n- 7: complement 2 (found in map!).\n**Result: [0, 1]**"
        ),
        (
            "Problem 34: Binary Search",
            "### Problem Overview\nFind the position of a target value within a sorted array. If it doesn't exist, return -1.\n\n"
            "### Core Concept\nDivide and Conquer. By halving the search space in each step, we achieve logarithmic time complexity $O(\log N)$.\n\n"
            "### Detailed Logic\n1. Initialize `low = 0` and `high = length - 1`.\n"
            "2. While `low <= high`:\n"
            "3. Calculate `mid = low + (high - low) / 2` (to prevent integer overflow).\n"
            "4. If `arr[mid]` is the target, return `mid`.\n"
            "5. If `target < arr[mid]`, update `high = mid - 1`.\n"
            "6. Else, update `low = mid + 1`.\n\n"
            "### Edge Case Notes\n- Array must be sorted for Binary Search to work.\n\n"
            "### Example Walkthrough\n**Input:** [1, 3, 5, 7, 9], target=3\n- mid = index 2 (5). 3 < 5, so search left.\n- mid = index 0.5 -> index 1 (3). 3 == 3. **Match!**"
        ),
        (
            "Problem 35: Remove Duplicates from Sorted Array",
            "### Problem Overview\nRemove duplicates from a sorted array in-place such that each element appears only once and returns the new length.\n\n"
            "### Core Concept\nSlow and Fast Pointers. This is the most efficient way to 'clean up' sorted data in-place.\n\n"
            "### Detailed Logic\n1. If the array is empty, return 0.\n"
            "2. Initialize a pointer `i = 0` (the slow pointer).\n"
            "3. Iterate through the array with pointer `j` from 1 to `length - 1`.\n"
            "4. If `arr[j]` is not equal to `arr[i]`, increment `i` and set `arr[i] = arr[j]`.\n"
            "5. Return `i + 1`.\n\n"
            "### Edge Case Notes\n- Array with all unique elements.\n- Array with all identical elements.\n\n"
            "### Example Walkthrough\n**Input:** [1, 1, 2]\n1. j=1: arr[1] == arr[0] (skip)\n2. j=2: arr[2] != arr[0] -> i becomes 1, arr[1] = 2.\n**Result: Length 2, Array: [1, 2]**"
        ),
(
            "Problem 36: Transpose of a Matrix",
            "### Problem Overview\nGiven a 2D matrix, flip the matrix over its main diagonal, switching its row and column indices.\n\n"
            "### Core Concept\nIndex Mapping. A value at `matrix[i][j]` moves to `matrix[j][i]`. This tests your understanding of coordinate systems.\n\n"
            "### Detailed Logic\n1. Iterate through the rows (i) and columns (j).\n"
            "2. For a square matrix, swap elements where `j > i` to avoid swapping them back to their original positions.\n"
            "3. For a rectangular matrix, create a new result matrix with swapped dimensions ($Rows \\times Cols$ becomes $Cols \\times Rows$).\n"
            "4. Fill the new matrix: `result[j][i] = original[i][j]`.\n\n"
            "### Edge Case Notes\n- Non-square (rectangular) matrices require careful memory allocation for the new dimensions.\n\n"
            "### Example Walkthrough\n**Input:** [[1,2],[3,4]]\n- (0,1) swaps with (1,0) -> 2 and 3 swap.\n**Result: [[1,3],[2,4]]**"
        ),
        (
            "Problem 37: Spiral Matrix Traversal",
            "### Problem Overview\nGiven a 2D matrix, return all elements in spiral order, starting from the top-left and moving clockwise.\n\n"
            "### Core Concept\nBoundary Shrinking. This problem tests your ability to maintain state across multiple directions (Right, Down, Left, Up).\n\n"
            "### Detailed Logic\n1. Define four boundaries: `top`, `bottom`, `left`, and `right`.\n"
            "2. While the boundaries don't cross:\n"
            "   - Traverse from `left` to `right` along the `top` row, then increment `top`.\n"
            "   - Traverse from `top` to `bottom` along the `right` column, then decrement `right`.\n"
            "   - Traverse from `right` to `left` along the `bottom` row (if still valid), then decrement `bottom`.\n"
            "   - Traverse from `bottom` to `top` along the `left` column (if still valid), then increment `left`.\n\n"
            "### Edge Case Notes\n- Always check if `top <= bottom` and `left <= right` before internal loops to avoid duplicate processing.\n\n"
            "### Example Walkthrough\n**Input:** [[1,2,3],[4,5,6],[7,8,9]]\n- Output: 1, 2, 3 (Top) -> 6, 9 (Right) -> 8, 7 (Bottom) -> 4 (Left) -> 5 (Center).\n**Result: [1,2,3,6,9,8,7,4,5]**"
        ),
        
        (
            "Problem 38: Search a 2D Matrix",
            "### Problem Overview\nDetermine if a target value exists in an $m \\times n$ matrix where rows and columns are sorted in ascending order.\n\n"
            "### Core Concept\nStep-wise Elimination. Instead of $O(N \\times M)$, you can achieve $O(N + M)$ by starting at a corner.\n\n"
            "### Detailed Logic\n1. Start at the top-right corner (row 0, last column).\n"
            "2. If the current value equals the target, return True.\n"
            "3. If the current value is greater than the target, move left (the current column cannot contain the target).\n"
            "4. If the current value is smaller than the target, move down (the current row cannot contain the target).\n"
            "5. Repeat until you find the target or move out of bounds.\n\n"
            "### Edge Case Notes\n- Starting at the top-left doesn't work because moving right and moving down both increase the value.\n\n"
            "### Example Walkthrough\n**Input:** Matrix with top-right 15, Target 10.\n- 15 > 10: Move Left.\n- New value 11 > 10: Move Left.\n- New value 7 < 10: Move Down.\n**Result: True (if found)**"
        ),
        (
            "Problem 39: Subarray Sum Equals K",
            "### Problem Overview\nFind the total number of continuous subarrays whose sum equals a given value `k`.\n\n"
            "### Core Concept\nPrefix Sums + Hashing. This turns a $O(N^2)$ problem into $O(N)$ by remembering previous sums.\n\n"
            "### Detailed Logic\n1. Maintain a running `current_sum`.\n"
            "2. Use a Hash Map to store how many times each `prefix_sum` has occurred (initialize with `{0: 1}`).\n"
            "3. For each element: Update `current_sum`.\n"
            "4. Check if `current_sum - k` exists in the Hash Map.\n"
            "5. If it does, add its frequency to your total count.\n"
            "6. Update the Hash Map with the new `current_sum`.\n\n"
            "### Edge Case Notes\n- Negative numbers in the array mean sums can decrease and increase again.\n\n"
            "### Example Walkthrough\n**Input:** [1, 1, 1], k=2\n- Sums: 1 (Map:{1:1}), 2 (Map:{2:1}, check 2-2=0, count=1), 3 (Map:{3:1}, check 3-2=1, count=2).\n**Result: 2**"
        ),
        (
            "Problem 40: Maximum Subarray (Kadane’s Algorithm)",
            "### Problem Overview\nFind the contiguous subarray (containing at least one number) which has the largest sum and return its sum.\n\n"
            "### Core Concept\nDynamic Programming (Local Max vs. Global Max). At each step, decide whether to include the current number in the previous sum or start fresh.\n\n"
            "### Detailed Logic\n1. Initialize `max_so_far` and `current_max` with the first element of the array.\n"
            "2. Iterate from the second element to the end.\n"
            "3. `current_max = max(current_element, current_max + current_element)`.\n"
            "4. `max_so_far = max(max_so_far, current_max)`.\n"
            "5. If `current_max` falls below 0, it won't help future sums, so it effectively resets when the next element is processed.\n\n"
            "### Edge Case Notes\n- If all numbers are negative, the result is the largest single number.\n\n"
            "### Example Walkthrough\n**Input:** [-2, 1, -3, 4, -1]\n- Current at 1: max(1, -2+1) = 1. Global = 1.\n- Current at -3: max(-3, 1-3) = -2. Global = 1.\n- Current at 4: max(4, -2+4) = 4. Global = 4.\n**Result: 4**"
        ),
        
        (
            "Problem 41: Best Time to Buy and Sell Stock",
            "### Problem Overview\nGiven an array of stock prices, find the maximum profit you can achieve by buying on one day and selling on a future day.\n\n"
            "### Core Concept\nOne-pass Min-Tracking. To maximize profit, you must find the lowest price to buy and the highest price after that point.\n\n"
            "### Detailed Logic\n1. Initialize `min_price` to infinity and `max_profit` to 0.\n"
            "2. Iterate through the prices.\n"
            "3. Update `min_price` if the current price is lower.\n"
            "4. Otherwise, calculate `current_profit = price - min_price`.\n"
            "5. Update `max_profit` if `current_profit` is higher.\n\n"
            "### Edge Case Notes\n- If prices only decrease, max profit remains 0.\n\n"
            "### Example Walkthrough\n**Input:** [7, 1, 5, 3, 6]\n- min_price becomes 1.\n- price 5: profit 4.\n- price 6: profit 5.\n**Result: 5**"
        ),
        (
            "Problem 42: Majority Element (Boyer-Moore)",
            "### Problem Overview\nFind the element that appears more than $n/2$ times in an array of size $n$.\n\n"
            "### Core Concept\nBoyer-Moore Voting Algorithm. This allows finding the majority in $O(N)$ time and $O(1)$ space by using a 'counter' that cancels out different elements.\n\n"
            "### Detailed Logic\n1. Initialize a `candidate` and a `count = 0`.\n"
            "2. Iterate through the array:\n"
            "   - If `count == 0`, set `candidate = current_element`.\n"
            "   - If `current_element == candidate`, increment `count`.\n"
            "   - Else, decrement `count`.\n"
            "3. The `candidate` remaining at the end is the majority element.\n\n"
            "### Edge Case Notes\n- The algorithm assumes a majority element always exists.\n\n"
            "### Example Walkthrough\n**Input:** [2, 2, 1, 1, 1, 2, 2]\n- (2, count 1) -> (2, count 2) -> (2, count 1) -> (2, count 0) -> (1, count 1) -> (1, count 0) -> (2, count 1).\n**Result: 2**"
        ),
        (
            "Problem 43: Merge Overlapping Intervals",
            "### Problem Overview\nGiven a collection of intervals, merge all overlapping intervals (e.g., [1,3] and [2,6] become [1,6]).\n\n"
            "### Core Concept\nSorting + Comparison. This tests your ability to order data and merge states based on overlapping boundaries.\n\n"
            "### Detailed Logic\n1. Sort the intervals based on their start times.\n"
            "2. Initialize an empty list `merged` and add the first interval.\n"
            "3. Iterate through the rest of the intervals:\n"
            "   - If the current interval starts BEFORE the last merged interval ends, they overlap.\n"
            "   - Update the end of the last merged interval to `max(last_end, current_end)`.\n"
            "   - Else, they don't overlap; add the current interval to `merged`.\n\n"
            "### Edge Case Notes\n- Intervals that are completely contained within others (e.g., [1,10] and [2,3]).\n\n"
            "### Example Walkthrough\n**Input:** [[1,3], [2,6], [8,10]]\n- [1,3] and [2,6] overlap since 2 < 3. Merge to [1,6].\n- [1,6] and [8,10] do not overlap since 8 > 6.\n**Result: [[1,6], [8,10]]**"
        ),
        (
            "Problem 44: Product of Array Except Self",
            "### Problem Overview\nFor each index `i`, return the product of all elements in the array except `arr[i]`, without using division.\n\n"
            "### Core Concept\nLeft and Right Prefix Products. This tests your ability to accumulate data from two directions.\n\n"
            "### Detailed Logic\n1. Create a result array where `res[i]` contains the product of all elements to the left of `i`.\n"
            "2. Iterate from right to left, maintaining a `right_product` variable.\n"
            "3. Multiply `res[i]` by `right_product`, then update `right_product` by multiplying it by `arr[i]`.\n\n"
            "### Edge Case Notes\n- Array containing one or more zeros.\n\n"
            "### Example Walkthrough\n**Input:** [1, 2, 3, 4]\n- Left products: [1, 1, 2, 6]\n- Right product for index 2 is 4: 2 * 4 = 8.\n- Right product for index 1 is 12: 1 * 12 = 12.\n**Result: [24, 12, 8, 6]**"
        ),
        (
            "Problem 45: Set Matrix Zeroes",
            "### Problem Overview\nIf an element in an $m \\times n$ matrix is 0, set its entire row and column to 0. Do this in-place.\n\n"
            "### Core Concept\nIn-place Marking. To avoid using $O(M \\times N)$ extra space, use the first row and first column as trackers.\n\n"
            "### Detailed Logic\n1. Determine if the first row or first column should eventually be zeroed.\n"
            "2. Use the first row and column to mark which other rows/cols contain a 0.\n"
            "3. Iterate through the rest of the matrix; if `matrix[i][j] == 0`, set `matrix[i][0] = 0` and `matrix[0][j] = 0`.\n"
            "4. Use these markers to update the rest of the matrix.\n"
            "5. Finally, update the first row/column based on the initial check.\n\n"
            "### Edge Case Notes\n- Be careful not to use the markers to zero out the markers themselves before you've finished reading them.\n\n"
            "### Example Walkthrough\n**Input:** [[1,1,1],[1,0,1],[1,1,1]]\n- Row 1 and Col 1 are marked as zero.\n- Final result zeroes out the middle cross.\n**Result: [[1,0,1],[0,0,0],[1,0,1]]**"
        ),

        (
            "Problem 46: Power Function (x^n)",
            "### Problem Overview\nImplement `pow(x, n)`, which calculates $x$ raised to the power $n$ (i.e., $x^n$).\n\n"
            "### Core Concept\nBinary Exponentiation (Exponentiation by Squaring). This reduces the time complexity from $O(N)$ to $O(\log N)$.\n\n"
            "### Detailed Logic\n1. Use the property: If $n$ is even, $x^n = (x^2)^{n/2}$. If $n$ is odd, $x^n = x \times (x^2)^{(n-1)/2}$.\n"
            "2. Handle negative powers: $x^{-n} = 1 / x^n$.\n"
            "3. Base Case: Any number to the power of 0 is 1.\n"
            "4. Recursively or iteratively square the base and halve the exponent.\n\n"
            "### Edge Case Notes\n- $n$ is a very large negative or positive integer (handle 32-bit overflow).\n- $x$ is 0 or 1.\n\n"
            "### Example Walkthrough\n**Input:** x=2.0, n=10\n- $2^{10} = (2^2)^5 = 4^5$\n- $4^5 = 4 \times (4^2)^2 = 4 \times 16^2 = 4 \times 256$.\n**Result: 1024**"
        ),
        (
            "Problem 47: Generate Parentheses",
            "### Problem Overview\nGiven $n$ pairs of parentheses, generate all combinations of well-formed parentheses.\n\n"
            "### Core Concept\nBacktracking with Constraints. You must ensure that at any point in the string, you never have more closing parentheses than opening ones.\n\n"
            "### Detailed Logic\n1. Use a recursive function that tracks the number of `open` and `close` brackets used.\n"
            "2. Base Case: If the length of the string is $2n$, add it to the results.\n"
            "3. Recursive Step 1: If `open < n`, add '(' and recurse.\n"
            "4. Recursive Step 2: If `close < open`, add ')' and recurse.\n"
            "5. This ensures the string is always prefix-valid.\n\n"
            "### Edge Case Notes\n- $n=1$ results in only `()`.\n\n"
            "### Example Walkthrough\n**Input:** n=2\n- '(' -> '((' -> '(())'\n- '(' -> '()' -> '()('\n**Result: ['(())', '()()']**"
        ),
        
        (
            "Problem 48: Climbing Stairs",
            "### Problem Overview\nYou are climbing a staircase that takes $n$ steps to reach the top. Each time you can either take 1 or 2 steps. In how many distinct ways can you climb to the top?\n\n"
            "### Core Concept\nDynamic Programming (Fibonacci Pattern). The number of ways to reach step $i$ is the sum of ways to reach $(i-1)$ and $(i-2)$.\n\n"
            "### Detailed Logic\n1. Base Cases: Step 1 = 1 way; Step 2 = 2 ways.\n"
            "2. For any step $i$, you could have arrived from the previous step or the step before that.\n"
            "3. Use a loop to calculate the sum iteratively to save space ($O(1)$ space).\n\n"
            "### Edge Case Notes\n- This is exactly the Fibonacci sequence offset by one position.\n\n"
            "### Example Walkthrough\n**Input:** n=3\n- Way 1: 1+1+1\n- Way 2: 1+2\n- Way 3: 2+1\n**Result: 3**"
        ),
        (
            "Problem 49: Permutations",
            "### Problem Overview\nGiven an array of distinct integers, return all possible permutations in any order.\n\n"
            "### Core Concept\nBacktracking (Swapping). This explores every possible leaf node in a decision tree where each level represents a position in the array.\n\n"
            "### Detailed Logic\n1. Use recursion with a 'start' index.\n"
            "2. For each index from 'start' to the end of the array, swap the current element with the 'start' element.\n"
            "3. Recurse for the next position (`start + 1`).\n"
            "4. **Backtrack:** Swap the elements back to their original positions to explore other branches.\n\n"
            "### Edge Case Notes\n- Total permutations for $N$ elements is $N!$.\n\n"
            "### Example Walkthrough\n**Input:** [1,2]\n- Swap(1,1) -> [1,2] -> Result: [1,2]\n- Swap(1,2) -> [2,1] -> Result: [2,1]\n**Result: [[1,2], [2,1]]**"
        ),
        (
            "Problem 50: Subsets (Power Set)",
            "### Problem Overview\nGiven an integer array of unique elements, return all possible subsets (the power set).\n\n"
            "### Core Concept\nCascading or Backtracking. Each element has two choices: to be included in the subset or not.\n\n"
            "### Detailed Logic\n1. Start with an empty subset: `[[]]`.\n"
            "2. For each number in the input array:\n"
            "3. Take all existing subsets and create new ones by adding the current number to them.\n"
            "4. Append these new subsets to your list.\n\n"
            "### Edge Case Notes\n- The empty set is always a subset.\n- Total subsets = $2^n$.\n\n"
            "### Example Walkthrough\n**Input:** [1,2]\n- Start: [[]]\n- Process 1: [[], [1]]\n- Process 2: [[], [1], [2], [1,2]]\n**Result: [[], [1], [2], [1,2]]**"
        ),
        (
            "Problem 51: Word Search",
            "### Problem Overview\nGiven an $m \times n$ grid of characters and a string `word`, return true if the word exists in the grid (adjacent cells horizontally or vertically).\n\n"
            "### Core Concept\nDepth-First Search (DFS) + Backtracking. Explore all 4 neighbors and 'mark' the current cell as visited.\n\n"
            "### Detailed Logic\n1. Iterate through every cell in the grid.\n"
            "2. If the cell matches the first letter of the word, start a DFS.\n"
            "3. In DFS: Check if the current character matches the word's current index.\n"
            "4. Temporarily change the cell character to '#' to mark it as visited.\n"
            "5. Recurse in 4 directions. If any direction returns true, the word is found.\n"
            "6. **Backtrack:** Change the cell character back to its original value.\n\n"
            "### Edge Case Notes\n- Cannot use the same letter cell more than once for a single word.\n\n"
            "### Example Walkthrough\n**Input:** Grid=[['A','B'],['C','D']], Word=\"AC\"\n- Start at (0,0) 'A'. Neighbors: 'B' and 'C'.\n- Move to 'C'. Index matches word length.\n**Result: True**"
        ),
        (
            "Problem 52: Merge Sort",
            "### Problem Overview\nSort an array using the Merge Sort algorithm.\n\n"
            "### Core Concept\nDivide and Conquer. This algorithm is stable and guarantees $O(N \log N)$ performance.\n\n"
            "### Detailed Logic\n1. **Divide:** Find the middle of the array and split it into two halves.\n"
            "2. **Conquer:** Recursively call Merge Sort on both halves.\n"
            "3. **Combine:** Merge the two sorted halves back together by comparing the smallest elements of each.\n\n"
            "### Edge Case Notes\n- Requires $O(N)$ extra space for the merging process.\n\n"
            "### Example Walkthrough\n**Input:** [38, 27, 43, 3]\n- Split: [38, 27] and [43, 3]\n- Sort halves: [27, 38] and [3, 43]\n- Merge: 3 vs 27 (3), 27 vs 43 (27), 38 vs 43 (38), 43.\n**Result: [3, 27, 38, 43]**"
        ),
        
        (
            "Problem 53: Quick Sort",
            "### Problem Overview\nSort an array using the Quick Sort algorithm.\n\n"
            "### Core Concept\nPartitioning. This is an in-place $O(N \log N)$ algorithm (average case) that uses a 'pivot' to divide the array.\n\n"
            "### Detailed Logic\n1. Pick an element as a 'pivot'.\n"
            "2. Partition: Move all elements smaller than the pivot to the left and larger elements to the right.\n"
            "3. Recursively apply the same logic to the left and right sub-arrays.\n"
            "4. The pivot ends up in its final sorted position after one partition.\n\n"
            "### Edge Case Notes\n- Worst case is $O(N^2)$ if the pivot is always the smallest or largest element.\n\n"
            "### Example Walkthrough\n**Input:** [10, 80, 30, 90, 40], Pivot=40\n- Partition: [10, 30, 40, 90, 80]. 40 is now fixed.\n- Recurse on [10, 30] and [90, 80].\n**Result: [10, 30, 40, 80, 90]**"
        ),
        (
            "Problem 54: Binary Search in Rotated Array",
            "### Problem Overview\nAn array sorted in ascending order is rotated at some pivot. Search for a target in $O(\log N)$ time.\n\n"
            "### Core Concept\nModified Binary Search. Even after rotation, at least one half of the array (left or right of mid) must be sorted.\n\n"
            "### Detailed Logic\n1. Find `mid`.\n"
            "2. If `arr[mid] == target`, return `mid`.\n"
            "3. Check if the left half is sorted (`arr[low] <= arr[mid]`).\n"
            "4. If sorted, check if target is within that range. If yes, move left; else move right.\n"
            "5. If left isn't sorted, the right half MUST be sorted. Perform similar range checks there.\n\n"
            "### Edge Case Notes\n- Array with duplicates requires a linear check in some cases ($O(N)$).\n\n"
            "### Example Walkthrough\n**Input:** [4,5,6,7,0,1,2], target=0\n- mid=7. Left [4,5,6,7] is sorted. 0 is not in [4..7].\n- Search right: [0,1,2]. mid=1. 0 < 1. Search left.\n**Result: Index 4**"
        ),
        (
            "Problem 55: Kth Largest Element",
            "### Problem Overview\nFind the $k$-th largest element in an unsorted array.\n\n"
            "### Core Concept\nQuickSelect or Min-Heap. Using a heap allows for $O(N \log K)$ complexity.\n\n"
            "### Detailed Logic\n1. Initialize a Min-Heap.\n"
            "2. Iterate through the array and add elements to the heap.\n"
            "3. If the heap size exceeds $k$, remove the smallest element (the root).\n"
            "4. After the loop, the root of the heap is the $k$-th largest element.\n\n"
            "### Edge Case Notes\n- If $k=1$, it's the maximum. If $k=N$, it's the minimum.\n\n"
            "### Example Walkthrough\n**Input:** [3,2,1,5,6,4], k=2\n- Heap: [3, 2] -> Add 1 (skip) -> Add 5 (Heap: [5, 3]) -> Add 6 (Heap: [6, 5]) -> Add 4 (skip).\n**Result: 5**"
        ),

        (
            "Problem 56: Reverse a Linked List",
            "### Problem Overview\nGiven the head of a singly linked list, reverse the list so that the tail becomes the head.\n\n"
            "### Core Concept\nPointer Reorientation. This tests your ability to manipulate memory addresses without losing the reference to the rest of the data structure.\n\n"
            "### Detailed Logic\n1. Initialize three pointers: `prev` as Null, `curr` as Head, and `next_node` as Null.\n"
            "2. Iterate through the list while `curr` is not Null.\n"
            "3. Store the next node to avoid losing it: `next_node = curr.next`.\n"
            "4. Reverse the link: `curr.next = prev`.\n"
            "5. Move pointers forward: `prev = curr`, `curr = next_node`.\n"
            "6. Return `prev` as the new head.\n\n"
            "### Edge Case Notes\n- Empty list or single-node list should return the input as is.\n\n"
            "### Example Walkthrough\n**Input:** 1 -> 2 -> 3\n- Step 1: 1 points to Null. `prev` is 1.\n- Step 2: 2 points to 1. `prev` is 2.\n- Step 3: 3 points to 2. `prev` is 3.\n**Result: 3 -> 2 -> 1**"
        ),
        
        (
            "Problem 57: Detect Cycle in a Linked List",
            "### Problem Overview\nDetermine if a linked list contains a cycle (a loop where a node points back to a previous node).\n\n"
            "### Core Concept\nFloyd’s Cycle-Finding Algorithm (Tortoise and Hare). This is an $O(N)$ time and $O(1)$ space solution.\n\n"
            "### Detailed Logic\n1. Initialize two pointers: `slow` and `fast`, both at the Head.\n"
            "2. Move `slow` by 1 step and `fast` by 2 steps.\n"
            "3. If there is a cycle, the `fast` pointer will eventually lap the `slow` pointer, and they will meet (`slow == fast`).\n"
            "4. If `fast` reaches Null, there is no cycle.\n\n"
            "### Edge Case Notes\n- A list with only one node pointing to itself.\n\n"
            "### Example Walkthrough\n**Input:** 1 -> 2 -> 3 -> 2 (cycle)\n- Step 1: slow=2, fast=3.\n- Step 2: slow=3, fast=3. **Match!**\n**Result: True**"
        ),
        (
            "Problem 58: Merge Two Sorted Lists",
            "### Problem Overview\nMerge two sorted linked lists into one sorted linked list.\n\n"
            "### Core Concept\nIterative Comparison. Similar to the 'Merge' step in Merge Sort, but performed on nodes rather than array indices.\n\n"
            "### Detailed Logic\n1. Create a `dummy` node to act as the starting point of the new list.\n"
            "2. Use a `tail` pointer to track the end of the new list.\n"
            "3. While both lists have nodes: compare the values.\n"
            "4. Attach the smaller node to `tail.next` and move that list's pointer forward.\n"
            "5. Once one list is exhausted, attach the remainder of the other list to `tail.next`.\n\n"
            "### Edge Case Notes\n- One or both lists being empty.\n\n"
            "### Example Walkthrough\n**Input:** L1: 1->3, L2: 2->4\n- Compare 1 and 2: New list 1 -> ...\n- Compare 3 and 2: New list 1 -> 2 -> ...\n**Result: 1 -> 2 -> 3 -> 4**"
        ),
        (
            "Problem 59: Remove Nth Node From End",
            "### Problem Overview\nRemove the $n$-th node from the end of a linked list and return its head.\n\n"
            "### Core Concept\nTwo-Pointer Gap. By maintaining a fixed distance between two pointers, you can find the target in a single pass.\n\n"
            "### Detailed Logic\n1. Use two pointers, `fast` and `slow`.\n"
            "2. Move `fast` pointer $n$ steps ahead.\n"
            "3. If `fast` is already Null, the head needs to be removed.\n"
            "4. Move both pointers together until `fast.next` is Null.\n"
            "5. `slow` will now be right BEFORE the node to be deleted.\n"
            "6. Update `slow.next = slow.next.next`.\n\n"
            "### Edge Case Notes\n- Removing the head of the list.\n- List with only one node.\n\n"
            "### Example Walkthrough\n**Input:** 1->2->3->4, n=2\n- Fast moves 2 steps to '2'.\n- Fast and Slow move until Fast is at '4'. Slow is at '2'.\n- Delete node after '2' (which is '3').\n**Result: 1 -> 2 -> 4**"
        ),
        (
            "Problem 60: Middle of the Linked List",
            "### Problem Overview\nFind the middle node of a linked list. If there are two middle nodes, return the second one.\n\n"
            "### Core Concept\nFast and Slow Pointers. When the fast pointer reaches the end, the slow pointer will be exactly at the midpoint.\n\n"
            "### Detailed Logic\n1. Initialize `slow` and `fast` at the head.\n"
            "2. While `fast` and `fast.next` are not Null:\n"
            "3. Move `slow` by 1 and `fast` by 2.\n"
            "4. When the loop ends, return `slow`.\n\n"
            "### Edge Case Notes\n- Even length lists: returns the second of the two middle nodes.\n\n"
            "### Example Walkthrough\n**Input:** 1->2->3->4->5\n- Step 1: slow=2, fast=3\n- Step 2: slow=3, fast=5\n**Result: Node 3**"
        ),
        (
            "Problem 61: Palindrome Linked List",
            "### Problem Overview\nDetermine if a singly linked list is a palindrome (reads the same forward and backward).\n\n"
            "### Core Concept\nReverse Second Half. This uses the 'Middle' logic and 'Reverse' logic combined.\n\n"
            "### Detailed Logic\n1. Find the middle of the list.\n"
            "2. Reverse the second half of the list starting from the middle.\n"
            "3. Compare the first half and the reversed second half node by node.\n"
            "4. If all values match, it is a palindrome.\n\n"
            "### Edge Case Notes\n- Empty list or single node (True).\n\n"
            "### Example Walkthrough\n**Input:** 1 -> 2 -> 2 -> 1\n- Middle is second 2. Reverse from there: 1 -> 2.\n- Compare [1, 2] with [1, 2].\n**Result: True**"
        ),
        (
            "Problem 62: Intersection of Two Linked Lists",
            "### Problem Overview\nGiven the heads of two singly linked lists, return the node at which the two lists intersect.\n\n"
            "### Core Concept\nPointer Switching. By equalizing the travel distance, the pointers must meet at the intersection.\n\n"
            "### Detailed Logic\n1. Initialize two pointers, `pA` at Head A and `pB` at Head B.\n"
            "2. Traverse the lists. When `pA` reaches the end, redirect it to Head B.\n"
            "3. When `pB` reaches the end, redirect it to Head A.\n"
            "4. If they intersect, they will meet at the intersection node because they both travel exactly $LengthA + LengthB$ distance.\n\n"
            "### Edge Case Notes\n- If no intersection, they will both meet at Null.\n\n"
            "### Example Walkthrough\n**Input:** A: [1,2,3], B: [4,3]. (Intersection at 3)\n- pA travels 1,2,3,4,3...\n- pB travels 4,3,1,2,3...\n- They meet at 3.\n**Result: Node 3**"
        ),
        
        (
            "Problem 63: Add Two Numbers",
            "### Problem Overview\nYou are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order.\n\n"
            "### Core Concept\nElementary Addition with Carry. This tests digit extraction and linked list construction.\n\n"
            "### Detailed Logic\n1. Initialize a `dummy` head and a `carry = 0`.\n"
            "2. While there are nodes in L1 or L2 or a carry remains:\n"
            "3. Sum = `val1 + val2 + carry`.\n"
            "4. Update `carry = sum / 10`.\n"
            "5. Create a new node with `sum % 10` and attach it to the result list.\n"
            "6. Move pointers forward.\n\n"
            "### Edge Case Notes\n- Lists of different lengths.\n- A final carry that requires an extra node (e.g., 99 + 1).\n\n"
            "### Example Walkthrough\n**Input:** (2->4) + (5->6) -> [2+5=7], [4+6=10, carry 1]\n**Result: 7 -> 0 -> 1**"
        ),
        (
            "Problem 64: Delete Node in a Linked List",
            "### Problem Overview\nDelete a node (except the tail) in a singly linked list, given only access to that node.\n\n"
            "### Core Concept\nValue Overwriting. Since you cannot access the previous node to change its `next` pointer, you must move the data instead.\n\n"
            "### Detailed Logic\n1. Copy the value from the next node into the current node.\n"
            "2. Set the current node's `next` pointer to point to the node AFTER the next node.\n"
            "3. Effectively, the next node is deleted while its 'spirit' (value) lives on in the current node.\n\n"
            "### Edge Case Notes\n- This cannot be used to delete the last node of the list.\n\n"
            "### Example Walkthrough\n**Input:** Node to delete is '5' in 4->5->1->9\n- Copy '1' into '5' -> 4->1->1->9\n- Skip the original '1' -> 4->1->9\n**Result: 4 -> 1 -> 9**"
        ),
        (
            "Problem 65: Sort List",
            "### Problem Overview\nSort a linked list in $O(N \log N)$ time using constant space complexity.\n\n"
            "### Core Concept\nMerge Sort for Lists. This uses 'Middle of List' to divide and 'Merge Two Sorted Lists' to combine.\n\n"
            "### Detailed Logic\n1. Base Case: If head is Null or head.next is Null, return head.\n"
            "2. Split the list into two halves using the Fast and Slow pointer method.\n"
            "3. Recursively sort each half.\n"
            "4. Merge the two sorted halves using the sorted merge function.\n\n"
            "### Edge Case Notes\n- Remember to set the end of the first half to Null to disconnect the two lists.\n\n"
            "### Example Walkthrough\n**Input:** 4->2->1->3\n- Split: [4,2] and [1,3]\n- Sort: [2,4] and [1,3]\n- Merge: 1->2->3->4\n**Result: 1 -> 2 -> 3 -> 4**"
        ),
        (
            "Problem 66: Implement Stack using Arrays",
            "### Problem Overview\nCreate a Stack data structure from scratch using a fixed-size or dynamic array.\n\n"
            "### Core Concept\nLIFO (Last-In-First-Out) logic. Access is restricted to the 'top' of the structure.\n\n"
            "### Detailed Logic\n1. Maintain a `top` index variable, initialized to -1.\n"
            "2. **Push:** Increment `top` and store the value at `arr[top]`.\n"
            "3. **Pop:** Retrieve the value at `arr[top]` and decrement `top`.\n"
            "4. **Peek:** Return `arr[top]` without removing it.\n\n"
            "### Edge Case Notes\n- Stack Overflow: Pushing to a full array.\n- Stack Underflow: Popping from an empty stack.\n\n"
            "### Example Walkthrough\n**Input:** Push(5), Push(10), Pop()\n- Push 5: top=0, arr=[5]\n- Push 10: top=1, arr=[5, 10]\n- Pop: Returns 10, top=0.\n**Result: 10**"
        ),
        (
            "Problem 67: Implement Queue using Arrays",
            "### Problem Overview\nCreate a Queue data structure using an array, ensuring elements are handled in the order they arrive.\n\n"
            "### Core Concept\nFIFO (First-In-First-Out). Elements enter at the 'rear' and leave from the 'front'.\n\n"
            "### Detailed Logic\n1. Maintain two pointers: `front` and `rear`.\n"
            "2. **Enqueue:** Add to the `rear` index and increment it.\n"
            "3. **Dequeue:** Retrieve from the `front` index and increment it.\n"
            "4. To optimize space, use a **Circular Queue** where `rear = (rear + 1) % size`.\n\n"
            "### Edge Case Notes\n- Queue Full vs. Queue Empty conditions.\n\n"
            "### Example Walkthrough\n**Input:** Enqueue(1), Enqueue(2), Dequeue()\n- Enqueue 1: [1], front=0, rear=1\n- Dequeue: Returns 1, front moves to index 1.\n**Result: 1**"
        ),
        
        (
            "Problem 68: Min Stack",
            "### Problem Overview\nDesign a stack that supports push, pop, top, and retrieving the minimum element in constant $O(1)$ time.\n\n"
            "### Core Concept\nAuxiliary State tracking. A second stack tracks the 'minimum so far' for every level of the main stack.\n\n"
            "### Detailed Logic\n1. Use two stacks: `mainStack` and `minStack`.\n"
            "2. **Push(x):** Push `x` to `mainStack`. Push `min(x, current_min)` to `minStack`.\n"
            "3. **Pop():** Pop from both stacks to keep them synchronized.\n"
            "4. **GetMin():** Simply return the top of `minStack`.\n\n"
            "### Edge Case Notes\n- Minimum element changes as you pop items.\n\n"
            "### Example Walkthrough\n**Input:** Push(3), Push(5), Push(2), GetMin()\n- mainStack: [3, 5, 2]\n- minStack: [3, 3, 2]\n**Result: 2**"
        ),
        (
            "Problem 69: Next Greater Element",
            "### Problem Overview\nFor each element in an array, find the first element to its right that is larger than it.\n\n"
            "### Core Concept\nMonotonic Stack. This pattern efficiently processes elements by maintaining a stack of 'unresolved' indices in decreasing order.\n\n"
            "### Detailed Logic\n1. Initialize a result array with -1.\n"
            "2. Iterate through the array from left to right.\n"
            "3. While the current element is greater than the element at the index on top of the stack:\n"
            "   - Pop the index and set its 'next greater' to the current element.\n"
            "4. Push the current index onto the stack.\n\n"
            "### Edge Case Notes\n- Elements with no greater value to their right remain -1.\n\n"
            "### Example Walkthrough\n**Input:** [4, 5, 2, 10]\n- 4: Push index 0.\n- 5: 5 > 4. Result[0] = 5. Push index 1.\n- 2: 2 < 5. Push index 2.\n- 10: 10 > 2 and 10 > 5. Result[2]=10, Result[1]=10.\n**Result: [5, 10, 10, -1]**"
        ),
        (
            "Problem 70: Implement Queue using Stacks",
            "### Problem Overview\nImplement a FIFO queue using only two LIFO stacks.\n\n"
            "### Core Concept\nAmortized Transfer. You flip the order of elements by pouring them from one stack into another.\n\n"
            "### Detailed Logic\n1. Use two stacks: `input` and `output`.\n"
            "2. **Push:** Always push to the `input` stack.\n"
            "3. **Pop/Peek:** If `output` is empty, pop all elements from `input` and push them into `output`.\n"
            "4. Pop from `output` stack.\n\n"
            "### Edge Case Notes\n- Efficient because each element is moved between stacks only once.\n\n"
            "### Example Walkthrough\n**Input:** Push(1), Push(2), Pop()\n- input: [1, 2], output: []\n- Transfer -> input: [], output: [2, 1]\n- Pop: Returns 1.\n**Result: 1**"
        ),
        (
            "Problem 71: Evaluate Reverse Polish Notation",
            "### Problem Overview\nEvaluate the value of an arithmetic expression in Postfix (RPN) notation (e.g., `[\"2\", \"1\", \"+\", \"3\", \"*\"]`).\n\n"
            "### Core Concept\nPostfix Stack Evaluation. Operators follow their operands.\n\n"
            "### Detailed Logic\n1. Iterate through the tokens.\n"
            "2. If it is a number, push it onto the stack.\n"
            "3. If it is an operator (+, -, *, /):\n"
            "   - Pop the top two numbers (`b`, then `a`).\n"
            "   - Perform the operation (`a operator b`).\n"
            "   - Push the result back onto the stack.\n\n"
            "### Edge Case Notes\n- Be careful with the order of operands in subtraction and division (the first one popped is the right-hand operand).\n\n"
            "### Example Walkthrough\n**Input:** [\"4\", \"13\", \"5\", \"/\", \"+\"]\n1. Push 4, 13, 5.\n2. \"/\": Pop 5, 13. 13/5 = 2. Push 2.\n3. \"+\": Pop 2, 4. 4+2 = 6. Push 6.\n**Result: 6**"
        ),
        (
            "Problem 72: Daily Temperatures",
            "### Problem Overview\nGiven an array of temperatures, return an array such that `res[i]` is the number of days you have to wait until a warmer temperature.\n\n"
            "### Core Concept\nMonotonic Decreasing Stack. Similar to 'Next Greater Element' but storing index distances.\n\n"
            "### Detailed Logic\n1. Initialize a result array of zeros.\n"
            "2. Create a stack to store indices.\n"
            "3. For each day `i`:\n"
            "4. While stack is not empty and `temp[i] > temp[stack_top]`:\n"
            "   - `idx = pop()`\n"
            "   - `res[idx] = i - idx`\n"
            "5. Push `i` onto the stack.\n\n"
            "### Edge Case Notes\n- If no warmer day exists, the value remains 0.\n\n"
            "### Example Walkthrough\n**Input:** [73, 74, 75, 71]\n- Day 0 (73): Push 0.\n- Day 1 (74): 74 > 73. res[0] = 1-0 = 1. Push 1.\n- Day 2 (75): 75 > 74. res[1] = 2-1 = 1. Push 2.\n**Result: [1, 1, 0, 0]**"
        ),
        (
            "Problem 73: Valid Parentheses (Advanced)",
            "### Problem Overview\nVerify if a string of brackets is valid, handling deep nesting and mixed types.\n\n"
            "### Core Concept\nBalanced Symbol Check. A stack ensures that the inner-most brackets are resolved first.\n\n"
            "### Detailed Logic\n1. Map closing brackets to opening ones: ` {')': '(', ']': '[', '}': '{'} `.\n"
            "2. Push openers to stack.\n"
            "3. On closer, pop stack; if it doesn't match the required opener, it's invalid.\n"
            "4. Result is True only if stack is empty at the end.\n\n"
            "### Edge Case Notes\n- String length should ideally be even.\n\n"
            "### Example Walkthrough\n**Input:** \"[{()}]\"\n- Result: True (Inner '()' closes, then '{}', then '[]')."
        ),
        (
            "Problem 74: Sort a Stack",
            "### Problem Overview\nSort a stack such that the smallest elements are on top using only stack operations and recursion.\n\n"
            "### Core Concept\nRecursive Insertion. This tests your ability to use the 'Call Stack' as temporary storage.\n\n"
            "### Detailed Logic\n1. `sortStack(stack)`: Pop the top element `x`. Recursively sort the remaining stack.\n"
            "2. `insertSorted(stack, x)`: If stack is empty or `x` is smaller than top, push `x`.\n"
            "3. Else, pop the top, recurse `insertSorted` for `x`, and then push the popped item back.\n\n"
            "### Edge Case Notes\n- Avoid using other data structures like arrays.\n\n"
            "### Example Walkthrough\n**Input:** Stack [3, 1, 2] (top is 2)\n- Pop 2, sort [3, 1]. Pop 1, sort [3].\n- Insert 1 into sorted [3] -> [3, 1].\n- Insert 2 into sorted [3, 1] -> [3, 2, 1].\n**Result: [3, 2, 1] (1 on top)**"
        ),
        (
            "Problem 75: Sliding Window Maximum",
            "### Problem Overview\nGiven an array and a window size $k$, find the maximum element in each sliding window.\n\n"
            "### Core Concept\nDeque (Double-Ended Queue). Maintain a monotonic queue of indices where values are in strictly decreasing order.\n\n"
            "### Detailed Logic\n1. Use a Deque to store indices of elements in the current window.\n"
            "2. For each new element: Remove indices from the back if their values are smaller than the new element.\n"
            "3. Add the new index to the back.\n"
            "4. Remove the front index if it has slid out of the window (`front < i - k + 1`).\n"
            "5. The value at the `front` of the Deque is the maximum for that window.\n\n"
            "### Edge Case Notes\n- $k=1$ results in the array itself.\n\n"
            "### Example Walkthrough\n**Input:** [1, 3, -1, -3], k=3\n- Window [1, 3, -1]: Deque contains index of 3 and -1. Max is 3.\n- Window [3, -1, -3]: Deque contains index of 3, -1, -3. Max is 3.\n**Result: [3, 3]**"
        ),
        (
            "Problem 76: Inorder Traversal",
            "### Problem Overview\nTraverse a binary tree and visit nodes in the order: Left Subtree -> Root -> Right Subtree.\n\n"
            "### Core Concept\nRecursive Depth-First Search (DFS). For a Binary Search Tree (BST), this traversal results in values being visited in sorted order.\n\n"
            "### Detailed Logic\n1. Base Case: If the current node is Null, return.\n"
            "2. Recursively call the function for the left child.\n"
            "3. Process/Print the current node's value.\n"
            "4. Recursively call the function for the right child.\n\n"
            "### Edge Case Notes\n- An empty tree (return an empty list).\n- A skewed tree (looks like a linked list).\n\n"
            "### Example Walkthrough\n**Input:** [1, null, 2, 3] (Root 1, Right 2, 2's Left 3)\n- Visit Left of 1 (Null).\n- Visit 1.\n- Visit Left of 2 (3).\n- Visit 2.\n**Result: [1, 3, 2]**"
        ),
        
        (
            "Problem 77: Preorder and Postorder Traversal",
            "### Problem Overview\nImplement Preorder (Root-Left-Right) and Postorder (Left-Right-Root) traversals.\n\n"
            "### Core Concept\nDFS Visit Priority. Preorder is often used to clone a tree, while Postorder is used to delete or evaluate a tree (like a directory size calculation).\n\n"
            "### Detailed Logic\n1. **Preorder:** Process Root first, then dive into children.\n2. **Postorder:** Process children completely before looking at the Root.\n3. Both follow the same recursive pattern as Inorder but change the 'Visit' line's position.\n\n"
            "### Edge Case Notes\n- For N nodes, all traversals take $O(N)$ time.\n\n"
            "### Example Walkthrough\n**Input:** [1, 2, 3]\n- Preorder: 1, 2, 3.\n- Postorder: 2, 3, 1."
        ),
        (
            "Problem 78: Maximum Depth of Binary Tree",
            "### Problem Overview\nFind the length of the longest path from the root node down to the farthest leaf node.\n\n"
            "### Core Concept\nHeight Calculation. The height of a node is $1 + \max(\text{height of left}, \text{height of right})$.\n\n"
            "### Detailed Logic\n1. Base Case: If node is Null, depth is 0.\n"
            "2. Recursively find the depth of the left subtree.\n"
            "3. Recursively find the depth of the right subtree.\n"
            "4. Return the maximum of the two results plus 1 (for the current level).\n\n"
            "### Edge Case Notes\n- A tree with only a root has a depth of 1.\n\n"
            "### Example Walkthrough\n**Input:** [3, 9, 20, null, null, 15, 7]\n- Left (9) depth is 1. Right (20) depth is 2 (due to 15, 7).\n- $1 + \max(1, 2) = 3$.\n**Result: 3**"
        ),
        (
            "Problem 79: Level Order Traversal (BFS)",
            "### Problem Overview\nVisit tree nodes level by level, from left to right (e.g., all nodes at depth 1, then all nodes at depth 2).\n\n"
            "### Core Concept\nBreadth-First Search (BFS) using a Queue. This explores the tree layer by layer instead of going deep.\n\n"
            "### Detailed Logic\n1. Initialize a Queue and add the Root.\n"
            "2. While the queue is not empty:\n"
            "3. Get the size of the queue (this is the number of nodes at the current level).\n"
            "4. Iterate through those nodes, popping them, adding their values to a list, and adding their children to the queue.\n\n"
            "### Edge Case Notes\n- Use a queue (FIFO) to maintain the correct order of levels.\n\n"
            "### Example Walkthrough\n**Input:** [3, 9, 20]\n- Level 0: [3]\n- Level 1: [9, 20]\n**Result: [[3], [9, 20]]**"
        ),
        
        (
            "Problem 80: Invert Binary Tree",
            "### Problem Overview\nFlip a binary tree so that the left and right children of every node are swapped (Mirror Image).\n\n"
            "### Core Concept\nRecursive Swapping. This is a classic test of your ability to manipulate tree pointers.\n\n"
            "### Detailed Logic\n1. Base Case: If node is Null, return Null.\n"
            "2. Swap the left child and right child of the current node.\n"
            "3. Recursively call invert for the new left child.\n"
            "4. Recursively call invert for the new right child.\n\n"
            "### Edge Case Notes\n- An empty tree or a single node remains unchanged.\n\n"
            "### Example Walkthrough\n**Input:** [4, 2, 7]\n- Swap 2 and 7.\n**Result: [4, 7, 2]**"
        ),
        (
            "Problem 81: Symmetric Tree",
            "### Problem Overview\nCheck if a binary tree is a mirror of itself (i.e., symmetric around its center).\n\n"
            "### Core Concept\nTwo-Tree Comparison. A tree is symmetric if its left subtree is a mirror of its right subtree.\n\n"
            "### Detailed Logic\n1. Use a helper function that takes two nodes (`L` and `R`).\n"
            "2. If both are Null, return True.\n"
            "3. If one is Null or values differ, return False.\n"
            "4. Check if `L.left` mirrors `R.right` AND `L.right` mirrors `R.left`.\n\n"
            "### Edge Case Notes\n- Even if values match, structural differences make it non-symmetric.\n\n"
            "### Example Walkthrough\n**Input:** [1, 2, 2, 3, 4, 4, 3]\n- Compare (2, 2): 3==3 and 4==4.\n**Result: True**"
        ),
        (
            "Problem 82: Search in a Binary Search Tree (BST)",
            "### Problem Overview\nFind a node with a specific value in a BST.\n\n"
            "### Core Concept\nBST Property: For any node, all values in the left subtree are smaller, and all values in the right subtree are larger.\n\n"
            "### Detailed Logic\n1. If Root is Null or matches target, return Root.\n"
            "2. If Target < Root.val, search the Left subtree.\n"
            "3. If Target > Root.val, search the Right subtree.\n"
            "4. This performs like Binary Search, with $O(\log N)$ average complexity.\n\n"
            "### Edge Case Notes\n- Worst case is $O(N)$ if the tree is unbalanced.\n\n"
            "### Example Walkthrough\n**Input:** BST with root 4, target 2.\n- 2 < 4: Move Left. Found 2.\n**Result: Node 2**"
        ),
        (
            "Problem 83: Validate Binary Search Tree",
            "### Problem Overview\nDetermine if a given binary tree is a valid BST.\n\n"
            "### Core Concept\nRange Constraints. Every node must be within a specific (min, max) range defined by its ancestors.\n\n"
            "### Detailed Logic\n1. Use a helper function `isValid(node, min, max)`.\n"
            "2. Initial call: `isValid(root, -infinity, +infinity)`.\n"
            "3. If node's value is not between `min` and `max`, return False.\n"
            "4. Recurse Left: update `max` to current node's value.\n"
            "5. Recurse Right: update `min` to current node's value.\n\n"
            "### Edge Case Notes\n- Simple local check (Left < Root < Right) is NOT enough; all left descendants must be smaller than the root.\n\n"
            "### Example Walkthrough\n**Input:** [5, 1, 4, null, null, 3, 6]\n- Node 4 is in the right of 5, but its child 3 is < 5.\n**Result: False**"
        ),
        (
            "Problem 84: Lowest Common Ancestor (LCA)",
            "### Problem Overview\nFind the lowest node in a tree that has both node $p$ and node $q$ as descendants.\n\n"
            "### Core Concept\nRecursive Bubbling. LCA is the node where $p$ and $q$ are split into different subtrees.\n\n"
            "### Detailed Logic\n1. If current node is Null, $p$, or $q$, return current node.\n"
            "2. Recurse Left and Right.\n"
            "3. If both recursions return non-null, the current node is the LCA.\n"
            "4. If only one returns non-null, return that one (the ancestor is further down).\n\n"
            "### Edge Case Notes\n- A node can be an ancestor of itself.\n\n"
            "### Example Walkthrough\n**Input:** root=3, p=5, q=1\n- 5 is left, 1 is right. LCA is 3.\n**Result: Node 3**"
        ),
        (
            "Problem 85: Balanced Binary Tree",
            "### Problem Overview\nDetermine if a binary tree is height-balanced (depth of the two subtrees of every node never differs by more than 1).\n\n"
            "### Core Concept\nBottom-up Height Check. This combines height calculation with a balance validation.\n\n"
            "### Detailed Logic\n1. Create a helper that returns height if balanced, else -1.\n"
            "2. For a node: get left height and right height.\n"
            "3. If either is -1 or `abs(left - right) > 1`, return -1.\n"
            "4. Else, return $1 + \max(left, right)$.\n\n"
            "### Edge Case Notes\n- An empty tree is balanced.\n\n"
            "### Example Walkthrough\n**Input:** [1, 2, 2, 3, null, null, 3, 4, null, null, 4]\n- Left subtree has depth 4, right has depth 2.\n- $|4 - 2| = 2 > 1$.\n**Result: False**"
        ),
        (
            "Problem 86: Number of Islands (DFS/BFS)",
            "### Problem Overview\nGiven an $m \\times n$ 2D binary grid representing a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and formed by connecting adjacent lands.\n\n"
            "### Core Concept\nConnected Components. This tests your ability to perform a traversal (DFS or BFS) to 'visit' and mark all parts of a single entity in a grid.\n\n"
            "### Detailed Logic\n1. Iterate through every cell in the grid.\n"
            "2. If a cell contains '1', you have found a new island. Increment your counter.\n"
            "3. Immediately trigger a DFS or BFS starting from that cell to find all connected '1's.\n"
            "4. During the traversal, change '1's to '0's (or a 'Visited' marker) to ensure you don't count the same island twice.\n"
            "5. The total count after the loop ends is the result.\n\n"
            "### Edge Case Notes\n- Grid with no land (0 islands).\n- Grid that is all land (1 island).\n\n"
            "### Example Walkthrough\n**Input:** \n110\n110\n001\n- First '1' found at (0,0). DFS clears the top-left 4 cells. Count=1.\n- Next '1' found at (2,2). DFS clears it. Count=2.\n**Result: 2**"
        ),
        
        (
            "Problem 87: Flood Fill",
            "### Problem Overview\nGiven a coordinate `(sr, sc)` in an image represented by a 2D array, and a `newColor`, change the color of the starting pixel and all its same-colored neighbors to `newColor`.\n\n"
            "### Core Concept\nArea Expansion. This is the logic behind the 'Paint Bucket' tool in graphics software.\n\n"
            "### Detailed Logic\n1. Store the `originalColor` of the starting pixel.\n"
            "2. If `originalColor` is already the `newColor`, return the image to avoid an infinite loop.\n"
            "3. Use a recursive function to check the 4-way neighbors (Up, Down, Left, Right).\n"
            "4. If a neighbor matches the `originalColor`, update it to `newColor` and recurse from there.\n\n"
            "### Edge Case Notes\n- Ensure you stay within grid boundaries.\n\n"
            "### Example Walkthrough\n**Input:** [[1,1,1],[1,1,0]], start=(1,1), color=2\n- All '1's connected to (1,1) turn into '2's.\n**Result: [[2,2,2],[2,2,0]]**"
        ),
        (
            "Problem 88: Coin Change (Dynamic Programming)",
            "### Problem Overview\nGiven an array of coin denominations and a total amount, find the fewest number of coins needed to make up that amount.\n\n"
            "### Core Concept\nOptimization (Overlapping Subproblems). Instead of trying every combination, you build the answer using previously calculated minimums.\n\n"
            "### Detailed Logic\n1. Create a `dp` array of size `amount + 1`, initialized with a large value (Infinity).\n"
            "2. Set `dp[0] = 0` (0 coins are needed for amount 0).\n"
            "3. For each amount `i` from 1 to `total_amount`:\n"
            "4. For each `coin` in denominations:\n"
            "   - If `coin <= i`, then `dp[i] = min(dp[i], dp[i - coin] + 1)`.\n"
            "5. If `dp[amount]` is still Infinity, the amount cannot be formed.\n\n"
            "### Edge Case Notes\n- This is a 'Bottom-Up' DP approach. $O(Amount \\times Coins)$ complexity.\n\n"
            "### Example Walkthrough\n**Input:** coins=[1, 2, 5], amount=11\n- To get 11: min of (11-1), (11-2), or (11-5) plus one coin.\n- Eventually finds 5+5+1.\n**Result: 3**"
        ),
        
        (
            "Problem 89: Longest Increasing Subsequence (LIS)",
            "### Problem Overview\nFind the length of the longest subsequence in an array such that all elements of the subsequence are sorted in ascending order.\n\n"
            "### Core Concept\nSequential Dependency. The LIS ending at index `i` depends on the LIS values of all indices `j < i` where `arr[j] < arr[i]`.\n\n"
            "### Detailed Logic\n1. Initialize a `dp` array of the same size as the input, filled with 1s (every element is a subsequence of length 1).\n"
            "2. Use a nested loop: `i` from 1 to $N$, and `j` from 0 up to `i`.\n"
            "3. If `arr[j] < arr[i]`, update `dp[i] = max(dp[i], dp[j] + 1)`.\n"
            "4. The maximum value in the `dp` array is the result.\n\n"
            "### Edge Case Notes\n- The subsequence does not need to be contiguous (unlike a subarray).\n\n"
            "### Example Walkthrough\n**Input:** [10, 9, 2, 5, 3, 7]\n- [2, 5, 7] or [2, 3, 7] are valid.\n**Result: 3**"
        ),
        (
            "Problem 90: Course Schedule (Topological Sort)",
            "### Problem Overview\nThere are $N$ courses to take, labeled 0 to $N-1$. Some courses have prerequisites (e.g., to take course 0 you must first take course 1). Can you finish all courses?\n\n"
            "### Core Concept\nDirected Acyclic Graph (DAG) and Cycle Detection. If the graph of prerequisites has a cycle, you can never finish.\n\n"
            "### Detailed Logic\n1. Build an adjacency list representing the graph.\n"
            "2. Use 'Kahn’s Algorithm' (BFS): Calculate the 'In-degree' (number of prerequisites) for each course.\n"
            "3. Add all courses with 0 in-degree to a queue.\n"
            "4. While the queue is not empty:\n"
            "   - Pop a course and increment a `count`.\n"
            "   - For each neighbor (courses that depend on this one), decrement their in-degree.\n"
            "   - If a neighbor's in-degree becomes 0, add it to the queue.\n"
            "5. If `count == N`, return True; else return False (a cycle exists).\n\n"
            "### Edge Case Notes\n- Disconnected graph: Some courses have no prerequisites at all.\n\n"
            "### Example Walkthrough\n**Input:** 2 courses, [[1,0]] (0 is prereq for 1)\n- In-degree: 0:0, 1:1. Queue: [0].\n- Pop 0. Count=1. 1's in-degree becomes 0. Queue: [1].\n- Pop 1. Count=2.\n**Result: True**"
        )








            # 🔁 CONTINUE UP TO PROBLEM 90
        ]

        # ======================================================

        start_date = datetime(2025, 12, 24)

        for index, (title, content) in enumerate(challenges):
            if index >= 90:
                break  # Hard safety guard

            date = (start_date + timedelta(days=index)).strftime("%Y-%m-%d")

            cursor.execute(
                """
                INSERT INTO questions (title, date, content, solution)
                VALUES (%s, %s, %s, %s)
                """,
                (title, date, content, "")
            )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ Success: {len(challenges)} problems inserted into Neon Database.")

    except Exception as e:
        print(f"❌ Error:", e)

if __name__ == "__main__":
    setup_professional_curriculum()
