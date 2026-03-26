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

        challenges=[
            (
            "Problem 91: Digit Sum Reduction",
            "### Problem Overview\nTake a number and repeatedly add all its digits together until the result becomes a single digit.\n\n"
            "### Core Concept\nIterative digit extraction and the concept of a digital root.\n\n"
            "### Detailed Logic\n1. While the number is greater than 9:\n"
            "2. Extract digits using `n % 10` and sum them.\n"
            "3. Update the number with this new sum and repeat.\n\n"
            "### Edge Case Notes\n- For input 0, the result is 0.\n- Can be solved mathematically using $1 + ((n - 1) \pmod 9)$.\n\n"
            "### Example Walkthrough\n**Input:** 98 -> 9+8=17 -> 1+7=8. **Result: 8**"
        ),
        (
            "Problem 92: Digit Product Reduction",
            "### Problem Overview\nMultiply all digits of the number together and repeat the process until only one digit remains.\n\n"
            "### Core Concept\nMultiplicative persistence and nested loop logic.\n\n"
            "### Detailed Logic\n1. While the number has more than one digit:\n"
            "2. Initialize `product = 1`.\n"
            "3. Extract each digit and multiply it to the product.\n"
            "4. Set the number to the product and continue.\n\n"
            "### Edge Case Notes\n- If the number contains a 0, the product immediately becomes 0.\n\n"
            "### Example Walkthrough\n**Input:** 39 -> 3*9=27 -> 2*7=14 -> 1*4=4. **Result: 4**"
        ),
        (
            "Problem 93: Largest Digit in a Number",
            "### Problem Overview\nExamine each digit of the given number and determine which digit is the largest.\n\n"
            "### Core Concept\nComparison logic and linear scanning of digits.\n\n"
            "### Detailed Logic\n1. Initialize `max_digit = 0`.\n"
            "2. Extract the last digit using `% 10`.\n"
            "3. Compare with `max_digit` and update if the current digit is larger.\n"
            "4. Divide the number by 10 and repeat until 0.\n\n"
            "### Edge Case Notes\n- For a single-digit number, the largest digit is the number itself.\n\n"
            "### Example Walkthrough\n**Input:** 472 -> Max(4, 7, 2) = 7. **Result: 7**"
        ),
        (
            "Problem 94: Smallest Digit in a Number",
            "### Problem Overview\nFind the smallest digit present in the given number.\n\n"
            "### Core Concept\nMinimum value tracking during digit extraction.\n\n"
            "### Detailed Logic\n1. Initialize `min_digit = 9`.\n"
            "2. Extract each digit using modulus.\n"
            "3. If the current digit is smaller than `min_digit`, update it.\n"
            "4. Continue until all digits are checked.\n\n"
            "### Edge Case Notes\n- If the number is 0, the smallest digit is 0.\n\n"
            "### Example Walkthrough\n**Input:** 518 -> Min(5, 1, 8) = 1. **Result: 1**"
        ),
        (
            "Problem 95: Difference Between Largest and Smallest Digit",
            "### Problem Overview\nDetermine the largest and smallest digits in a number, then calculate their difference.\n\n"
            "### Core Concept\nCombined comparison logic and arithmetic subtraction.\n\n"
            "### Detailed Logic\n1. Track both `max_val` and `min_val` while looping through digits.\n"
            "2. After the loop, calculate `diff = max_val - min_val`.\n\n"
            "### Edge Case Notes\n- If all digits are the same (e.g., 111), the difference is 0.\n\n"
            "### Example Walkthrough\n**Input:** 291 -> Max=9, Min=1. 9 - 1 = 8. **Result: 8**"
        ),
        (
            "Problem 96: Count Digits Greater Than Five",
            "### Problem Overview\nCheck each digit of the number and count how many digits are greater than 5.\n\n"
            "### Core Concept\nConditional counting within a digit extraction loop.\n\n"
            "### Detailed Logic\n1. Initialize `count = 0`.\n"
            "2. Extract each digit.\n"
            "3. If `digit > 5`, increment `count`.\n\n"
            "### Edge Case Notes\n- Digits equal to 5 are not counted.\n\n"
            "### Example Walkthrough\n**Input:** 648 -> 6 > 5 (Yes), 4 > 5 (No), 8 > 5 (Yes). **Count: 2**"
        ),
        (
            "Problem 97: Check Strictly Increasing Digits",
            "### Problem Overview\nVerify whether every digit in the number is strictly greater than the digit to its left.\n\n"
            "### Core Concept\nSequence validation and digit-to-digit comparison.\n\n"
            "### Detailed Logic\n1. Traverse digits from right to left.\n"
            "2. Compare the current digit with the next digit (the one to its left).\n"
            "3. If the right digit is not greater than the left digit at any point, return False.\n\n"
            "### Edge Case Notes\n- Single-digit numbers are strictly increasing by default.\n\n"
            "### Example Walkthrough\n**Input:** 123 -> 1 < 2 < 3. **Result: True**"
        ),
        (
            "Problem 98: Check Strictly Decreasing Digits",
            "### Problem Overview\nDetermine whether every digit is smaller than the digit before (to the left of) it.\n\n"
            "### Core Concept\nMonotonic sequence verification.\n\n"
            "### Detailed Logic\n1. Compare consecutive digits.\n"
            "2. Ensure each subsequent digit (moving left to right) is less than the previous one.\n\n"
            "### Edge Case Notes\n- Numbers like 321 are strictly decreasing; 322 is not.\n\n"
            "### Example Walkthrough\n**Input:** 542 -> 5 > 4 > 2. **Result: True**"
        ),
        (
            "Problem 99: Check Exactly One Even Digit",
            "### Problem Overview\nAnalyze all digits of the number and verify if exactly one of them is even.\n\n"
            "### Core Concept\nParity checking and frequency counting.\n\n"
            "### Detailed Logic\n1. Initialize `even_count = 0`.\n"
            "2. For each digit, check if `digit % 2 == 0`.\n"
            "3. Increment `even_count` if true.\n"
            "4. Result is True only if `even_count == 1`.\n\n"
            "### Edge Case Notes\n- Zero is considered an even digit.\n\n"
            "### Example Walkthrough\n**Input:** 134 -> Digits: 1(O), 3(O), 4(E). Even count = 1. **Result: True**"
        ),
        (
            "Problem 100: Sum of Digits at Even Positions",
            "### Problem Overview\nTreat the number as a sequence and sum the digits located at even index positions (2nd, 4th, etc.).\n\n"
            "### Core Concept\nPosition tracking during digit traversal.\n\n"
            "### Detailed Logic\n1. Convert number to a string or use a counter while extracting digits.\n"
            "2. Maintain a `position` variable starting from 1.\n"
            "3. If `position % 2 == 0`, add the digit to `total_sum`.\n\n"
            "### Edge Case Notes\n- Clarify if positions are counted from the left or right (usually left-to-right 1-indexed).\n\n"
            "### Example Walkthrough\n**Input:** 1234 -> Positions: 1(1), 2(2), 3(3), 4(4). Sum: 2 + 4 = 6. **Result: 6**"
        ),
        (
            "Problem 101: Check Harshad Number",
            "### Problem Overview\nA Harshad number (or Niven number) is an integer that is divisible by the sum of its digits.\n\n"
            "### Core Concept\nDigit summation and divisibility testing.\n\n"
            "### Detailed Logic\n1. Calculate the sum of all digits of the number $N$.\n"
            "2. Check if $N \pmod{\text{sum}} == 0$.\n"
            "3. If the remainder is zero, it is a Harshad number.\n\n"
            "### Edge Case Notes\n- All single-digit numbers from 1-9 are Harshad numbers.\n- Division by zero must be avoided (though digit sums are $>0$ for $N>0$).\n\n"
            "### Example Walkthrough\n**Input:** 18 -> Digit sum: 1+8=9. 18 is divisible by 9. **Result: True**"
        ),
        (
            "Problem 102: Check Neon Number",
            "### Problem Overview\nA Neon number is a number where the sum of the digits of its square equals the original number.\n\n"
            "### Core Concept\nPower operations combined with digit extraction logic.\n\n"
            "### Detailed Logic\n1. Calculate the square of the number ($N^2$).\n"
            "2. Extract and sum the digits of the resulting square.\n"
            "3. Compare this sum to the original number $N$.\n\n"
            "### Edge Case Notes\n- 9 is a famous Neon number ($9^2=81$, $8+1=9$). 0 and 1 are also Neon numbers.\n\n"
            "### Example Walkthrough\n**Input:** 9 -> Square: 81. Sum: 8+1=9. **Result: True**"
        ),
        (
            "Problem 103: Check Spy Number",
            "### Problem Overview\nA Spy number is a number where the sum of its digits equals the product of its digits.\n\n"
            "### Core Concept\nSimultaneous tracking of additive and multiplicative properties of digits.\n\n"
            "### Detailed Logic\n1. Initialize `sum = 0` and `product = 1`.\n"
            "2. Iterate through digits: add to `sum`, multiply into `product`.\n"
            "3. Check if `sum == product`.\n\n"
            "### Edge Case Notes\n- Numbers containing '0' will always have a digit product of 0.\n\n"
            "### Example Walkthrough\n**Input:** 1124 -> Sum: 1+1+2+4=8. Product: 1*1*2*4=8. **Result: True**"
        ),
        (
            "Problem 104: Check Automorphic Number",
            "### Problem Overview\nAn Automorphic number is a number whose square ends with the same digits as the number itself.\n\n"
            "### Core Concept\nSuffix verification using modulus based on the number of digits.\n\n"
            "### Detailed Logic\n1. Square the number $N$.\n"
            "2. Determine the number of digits in $N$ (let's call it $k$).\n"
            "3. Extract the last $k$ digits of the square using $Square \pmod{10^k}$.\n"
            "4. Compare the result with $N$.\n\n"
            "### Edge Case Notes\n- Example: 25 squared is 625. It ends in 25.\n\n"
            "### Example Walkthrough\n**Input:** 5 -> Square: 25. Ends in 5. **Result: True**"
        ),
        (
            "Problem 105: Check if Digit Sum is Prime",
            "### Problem Overview\nCalculate the sum of all digits and determine if that resulting sum is a prime number.\n\n"
            "### Core Concept\nNested logic: digit extraction followed by a primality test.\n\n"
            "### Detailed Logic\n1. Sum all digits of the number.\n"
            "2. Run a primality test on the sum: check if it has divisors other than 1 and itself.\n"
            "3. Remember that 1 is not prime.\n\n"
            "### Edge Case Notes\n- If digit sum is 2, it is prime. If digit sum is 1, it is not.\n\n"
            "### Example Walkthrough\n**Input:** 11 -> Digit sum: 2. 2 is prime. **Result: True**"
        ),
        (
            "Problem 106: Difference Between Digit Sum and Digit Product",
            "### Problem Overview\nCalculate the sum and product of digits separately, then find the absolute difference.\n\n"
            "### Core Concept\nArithmetic processing of extracted digits.\n\n"
            "### Detailed Logic\n1. Find `digit_sum` by adding all digits.\n"
            "2. Find `digit_product` by multiplying all digits.\n"
            "3. Return $|digit\_sum - digit\_product|$.\n\n"
            "### Edge Case Notes\n- The result should always be non-negative (absolute difference).\n\n"
            "### Example Walkthrough\n**Input:** 123 -> Sum: 6. Product: 6. Difference: 0. **Result: 0**"
        ),
        (
            "Problem 107: Palindrome After Removing Middle Digit",
            "### Problem Overview\nRemove the middle digit of a number and check if the remaining number is a palindrome.\n\n"
            "### Core Concept\nPositional manipulation and string/array slicing.\n\n"
            "### Detailed Logic\n1. Convert number to a string to easily locate the middle index.\n"
            "2. Remove the character at the middle index.\n"
            "3. Check if the remaining string reads the same forwards and backwards.\n\n"
            "### Edge Case Notes\n- For even-length numbers, define which 'middle' digit to remove or if it applies only to odd lengths.\n\n"
            "### Example Walkthrough\n**Input:** 12321 -> Remove '3' -> '1221'. '1221' is a palindrome. **Result: True**"
        ),
        (
            "Problem 108: Equal Half Digit Sum",
            "### Problem Overview\nSplit the digits of an even-length number into two halves and compare their sums.\n\n"
            "### Core Concept\nData partitioning and localized summation.\n\n"
            "### Detailed Logic\n1. Count total digits. If odd, handle accordingly (usually ignore middle or return False).\n"
            "2. Sum digits of the first half.\n"
            "3. Sum digits of the second half.\n"
            "4. Check if `sum1 == sum2`.\n\n"
            "### Edge Case Notes\n- Often called 'Lucky Numbers' in some contexts.\n\n"
            "### Example Walkthrough\n**Input:** 1230 -> Half 1: 1+2=3. Half 2: 3+0=3. **Result: True**"
        ),
        (
            "Problem 109: Count Digits Dividing the Number",
            "### Problem Overview\nCheck each digit of the number to see if it can divide the original number without a remainder.\n\n"
            "### Core Concept\nDivisibility rules and iteration.\n\n"
            "### Detailed Logic\n1. Iterate through each digit of the number.\n"
            "2. If the digit is not 0 and $OriginalNumber \pmod{digit} == 0$, increment counter.\n\n"
            "### Edge Case Notes\n- Must skip '0' digits to avoid 'Division by Zero' errors.\n\n"
            "### Example Walkthrough\n**Input:** 12 -> 1 divides 12 (Yes), 2 divides 12 (Yes). **Count: 2**"
        ),
        (
            "Problem 110: Even or Odd Sum of Squared Digits",
            "### Problem Overview\nSquare each digit, sum them up, and determine if the final total is even or odd.\n\n"
            "### Core Concept\nParity logic applied to powers and sums.\n\n"
            "### Detailed Logic\n1. For each digit, calculate $digit^2$.\n"
            "2. Maintain a running total of these squares.\n"
            "3. Check if `total % 2 == 0` (Even) or not (Odd).\n\n"
            "### Edge Case Notes\n- The square of an even digit is always even; square of an odd digit is always odd.\n\n"
            "### Example Walkthrough\n**Input:** 12 -> $1^2 + 2^2 = 1 + 4 = 5$. 5 is Odd. **Result: Odd**"
        ),
        (
            "Problem 111: Repeated Digit Sum Until Prime",
            "### Problem Overview\nRepeatedly compute the sum of the digits of a number until the resulting sum is a prime number.\n\n"
            "### Core Concept\nRecursive or iterative digit summation paired with primality testing.\n\n"
            "### Detailed Logic\n1. Calculate the sum of digits of $N$.\n"
            "2. Check if the sum is prime.\n"
            "3. If not prime, treat the sum as the new $N$ and repeat the process.\n"
            "4. If the sum becomes a single digit that is not prime (like 1, 4, 6, 8, 9) and cannot be reduced further, the condition may be impossible.\n\n"
            "### Edge Case Notes\n- Prime numbers are typically defined for integers $> 1$.\n\n"
            "### Example Walkthrough\n**Input:** 15 -> 1+5=6 (Not Prime) -> 6 is not prime. (Process continues or stops based on constraints)."
        ),
        (
            "Problem 112: Palindrome After Reverse and Add",
            "### Problem Overview\nReverse the digits of a number, add it to the original, and check if the result is a palindrome.\n\n"
            "### Core Concept\nNumeric reversal and symmetry verification.\n\n"
            "### Detailed Logic\n1. Reverse the digits of $N$ to get $N_{rev}$.\n"
            "2. Calculate $Sum = N + N_{rev}$.\n"
            "3. Check if $Sum$ reads the same forward and backward.\n\n"
            "### Edge Case Notes\n- This is related to the '196-algorithm' (though most numbers reach a palindrome quickly).\n\n"
            "### Example Walkthrough\n**Input:** 121 -> $121 + 121 = 242$. 242 is a palindrome. **Result: True**"
        ),
        (
            "Problem 113: Product of Digits Divisible by Digit Sum",
            "### Problem Overview\nCalculate both the sum and the product of the digits and check if the product is divisible by the sum.\n\n"
            "### Core Concept\nDivisibility logic using multiple digit-derived properties.\n\n"
            "### Detailed Logic\n1. Iterate through digits to calculate `total_sum` and `total_product`.\n"
            "2. Check if `total_sum` is not zero.\n"
            "3. Verify if `total_product % total_sum == 0`.\n\n"
            "### Edge Case Notes\n- If the digit sum is 0 (for input 0), divisibility is undefined.\n\n"
            "### Example Walkthrough\n**Input:** 12 -> Sum: 3, Product: 2. 2 is not divisible by 3. **Result: False**"
        ),
        (
            "Problem 114: Self-Dividing Number Check",
            "### Problem Overview\nA self-dividing number is a number that is divisible by every every one of its digits.\n\n"
            "### Core Concept\nUniversal divisibility across all constituent digits.\n\n"
            "### Detailed Logic\n1. Extract every digit of the number.\n"
            "2. If any digit is 0, it is not self-dividing (cannot divide by zero).\n"
            "3. If the original number is not divisible by any of its digits, return False.\n\n"
            "### Edge Case Notes\n- 128 is self-dividing: $128 \pmod 1 == 0$, $128 \pmod 2 == 0$, $128 \pmod 8 == 0$.\n\n"
            "### Example Walkthrough\n**Input:** 24 -> 24/2 (Yes), 24/4 (Yes). **Result: True**"
        ),
        (
            "Problem 115: Square Ends With Same Digits",
            "### Problem Overview\nSquare the given number and verify if the square ends with the same sequence of digits as the original number.\n\n"
            "### Core Concept\nPower operations and suffix matching.\n\n"
            "### Detailed Logic\n1. Compute $S = N^2$.\n"
            "2. Convert $N$ and $S$ to strings or use $10^k$ modulus logic.\n"
            "3. Check if $S$ ends with $N$.\n\n"
            "### Edge Case Notes\n- This is the definition of Automorphic numbers.\n\n"
            "### Example Walkthrough\n**Input:** 76 -> $76^2 = 5776$. Ends in 76. **Result: True**"
        ),
        (
            "Problem 116: Next Number With Same Digit Sum",
            "### Problem Overview\nFind the smallest integer greater than $N$ that has a digit sum equal to the digit sum of $N$.\n\n"
            "### Core Concept\nBrute force search or greedy incrementing with state comparison.\n\n"
            "### Detailed Logic\n1. Calculate `target_sum` of digits of $N$.\n"
            "2. Start a loop from $N + 1$.\n"
            "3. For each number, calculate its digit sum.\n"
            "4. Break and return the first number that matches `target_sum`.\n\n"
            "### Edge Case Notes\n- The search space can be large, but the next number usually appears relatively soon.\n\n"
            "### Example Walkthrough\n**Input:** 19 (Sum=10) -> Next is 28 (Sum=10). **Result: 28**"
        ),
        (
            "Problem 117: Symmetric Digit Frequency",
            "### Problem Overview\nCheck whether the frequency of digits forms a symmetric pattern (palindrome-like) when looking at the digits from both ends.\n\n"
            "### Core Concept\nFrequency mapping and symmetry testing.\n\n"
            "### Detailed Logic\n1. Treat the number's digits as a sequence.\n"
            "2. Check if the digit at index $i$ is the same as the digit at index $len-1-i$.\n\n"
            "### Edge Case Notes\n- This is essentially a standard Palindrome check applied specifically to digit frequency positions.\n\n"
            "### Example Walkthrough\n**Input:** 1221 -> 1=1, 2=2. **Result: True**"
        ),
        (
            "Problem 118: Split Number With Equal Digit Sum",
            "### Problem Overview\nDetermine if the digits of a number can be split at some point into two parts such that the sum of the left part equals the sum of the right part.\n\n"
            "### Core Concept\nPrefix and suffix sum comparison.\n\n"
            "### Detailed Logic\n1. Iterate through possible split points (e.g., after 1st digit, after 2nd, etc.).\n"
            "2. For each point, calculate the sum of digits to the left and to the right.\n"
            "3. If any split yields equal sums, return True.\n\n"
            "### Edge Case Notes\n- Requires at least two digits to perform a split.\n\n"
            "### Example Walkthrough\n**Input:** 1230 -> (1+2=3) and (3+0=3). **Result: True**"
        ),
        (
            "Problem 119: Digits Form Arithmetic Progression",
            "### Problem Overview\nCheck if the difference between all consecutive digits in a number is constant.\n\n"
            "### Core Concept\nArithmetic Progression (AP) verification.\n\n"
            "### Detailed Logic\n1. Extract all digits.\n"
            "2. Calculate the common difference $d = digit[1] - digit[0]$.\n"
            "3. Verify if $digit[i] - digit[i-1] == d$ for all $i$.\n\n"
            "### Edge Case Notes\n- Single-digit and two-digit numbers always satisfy this.\n\n"
            "### Example Walkthrough\n**Input:** 135 -> $3-1=2$, $5-3=2$. Constant difference 2. **Result: True**"
        ),
        (
            "Problem 120: Constant Digit Difference Pattern",
            "### Problem Overview\nVerify if the absolute difference between every consecutive digit is exactly the same.\n\n"
            "### Core Concept\nPattern recognition and absolute difference consistency.\n\n"
            "### Detailed Logic\n1. Extract digits.\n"
            "2. Calculate absolute difference $|digit[i] - digit[i-1]|$.\n"
            "3. Ensure this value is the same for all consecutive pairs.\n\n"
            "### Edge Case Notes\n- Similar to AP but uses absolute values (e.g., 131 has a constant absolute difference of 2).\n\n"
            "### Example Walkthrough\n**Input:** 131 -> $|3-1|=2$, $|1-3|=2$. **Result: True**"
        ),
        (
            "Problem 121: Check if Number is Power of Two",
            "### Problem Overview\nDetermine if a given integer is a power of two (e.g., 1, 2, 4, 8, 16...).\n\n"
            "### Core Concept\nLogarithmic properties or bit manipulation.\n\n"
            "### Detailed Logic\n1. If $N \leq 0$, return False.\n"
            "2. Use the bitwise trick: $(n \& (n - 1)) == 0$.\n"
            "3. Alternatively, keep dividing by 2; if you reach 1 without remainders, it is a power of 2.\n\n"
            "### Edge Case Notes\n- 1 is $2^0$, so it returns True.\n\n"
            "### Example Walkthrough\n**Input:** 16 -> $16/2=8, 8/2=4, 4/2=2, 2/2=1$. **Result: True**"
        ),
        (
            "Problem 122: Two Numbers Same Digit Set",
            "### Problem Overview\nCheck whether two given numbers contain the exact same set of digits, regardless of their order.\n\n"
            "### Core Concept\nSet comparison or frequency mapping.\n\n"
            "### Detailed Logic\n1. Convert both numbers to strings or lists of digits.\n"
            "2. Sort both lists and compare them, or use a frequency hash map.\n"
            "3. If the collections match perfectly, return True.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the digit sets are identical, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 123, 312 -> Sorted: [1,2,3], [1,2,3]. **Result: True**"
        ),
        (
            "Problem 123: Number With Unique Digits",
            "### Problem Overview\nVerify whether every digit in a number appears only once.\n\n"
            "### Core Concept\nUniqueness validation using Sets.\n\n"
            "### Detailed Logic\n1. Extract all digits from the number.\n"
            "2. Compare the count of total digits with the count of unique digits (using a Set).\n"
            "3. If counts are equal, no digits are repeated.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if all digits are unique, `False` if any digit repeats).\n\n"
            "### Example Walkthrough\n**Input:** 1234 -> Unique. **Result: True** | **Input:** 121 -> '1' repeats. **Result: False**"
        ),
        (
            "Problem 124: Mirror Digit Check",
            "### Problem Overview\nCompare a number with its reversed (mirror) version to see if they are identical.\n\n"
            "### Core Concept\nSymmetry verification (Palindrome logic).\n\n"
            "### Detailed Logic\n1. Reverse the digits of the number.\n"
            "2. Compare the original number with the reversed number.\n"
            "3. Return True if they are the same.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the number is a palindrome, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 121 -> Reversed: 121. **Result: True**"
        ),
        (
            "Problem 125: First Repeating Digit",
            "### Problem Overview\nIdentify the first digit (from left to right) that has already appeared previously in the number.\n\n"
            "### Core Concept\nMembership tracking using a 'seen' set.\n\n"
            "### Detailed Logic\n1. Iterate through the digits from left to right.\n"
            "2. Store each digit in a set as you go.\n"
            "3. If you encounter a digit already in the set, that is your first repeating digit.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The digit that repeats first) or `-1` if none repeat.\n\n"
            "### Example Walkthrough\n**Input:** 52325 -> 5(new), 2(new), 3(new), 2(already seen!). **Result: 2**"
        ),
        (
            "Problem 126: Most Frequent Digit",
            "### Problem Overview\nFind the digit that occurs the highest number of times within the number.\n\n"
            "### Core Concept\nFrequency counting and maximum value tracking.\n\n"
            "### Detailed Logic\n1. Create a frequency map (0-9) for the digits.\n"
            "2. Iterate through the number and increment counts.\n"
            "3. Find the digit with the maximum count. If there is a tie, usually return the smaller digit.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The most frequent digit).\n\n"
            "### Example Walkthrough\n**Input:** 112223 -> 1 appears twice, 2 appears three times, 3 appears once. **Result: 2**"
        ),
        (
            "Problem 127: Least Frequent Digit",
            "### Problem Overview\nDetermine which digit appears the fewest times in the number (ignoring digits not present at all).\n\n"
            "### Core Concept\nFrequency counting and minimum value tracking.\n\n"
            "### Detailed Logic\n1. Count occurrences of each digit present.\n"
            "2. Identify the digit with the lowest non-zero frequency.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The least frequent digit).\n\n"
            "### Example Walkthrough\n**Input:** 44555 -> 4 appears twice, 5 appears three times. **Result: 4**"
        ),
        (
            "Problem 128: Adjacent Digits Equal",
            "### Problem Overview\nCheck if there are any two identical digits sitting right next to each other.\n\n"
            "### Core Concept\nNeighbor comparison in a sequence.\n\n"
            "### Detailed Logic\n1. Loop through the digits from index 0 to $len-2$.\n"
            "2. Compare `digit[i]` with `digit[i+1]`.\n"
            "3. If any match is found, return True.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a neighbor match exists, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1223 -> 2 and 2 are adjacent. **Result: True**"
        ),
        (
            "Problem 129: Alternating Even Odd Pattern",
            "### Problem Overview\nVerify whether the digits alternate perfectly between even and odd parity.\n\n"
            "### Core Concept\nParity sequence validation.\n\n"
            "### Detailed Logic\n1. Check the parity of the first digit.\n"
            "2. Every subsequent digit must have the opposite parity of the previous one.\n"
            "3. If any pair has the same parity, the pattern is broken.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the pattern holds, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1234 -> Odd, Even, Odd, Even. **Result: True**"
        ),
        (
            "Problem 130: Count Increasing Pairs",
            "### Problem Overview\nCount how many times a digit is smaller than the one immediately following it.\n\n"
            "### Core Concept\nRelative comparison in a sequence.\n\n"
            "### Detailed Logic\n1. Iterate through digits.\n"
            "2. If `digit[i] < digit[i+1]`, increment the counter.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The total count of increasing pairs).\n\n"
            "### Example Walkthrough\n**Input:** 1324 -> (1<3) and (2<4). **Result: 2**"
        ),
        (
            "Problem 131: Count Decreasing Pairs",
            "### Problem Overview\nCount how many times a digit is larger than the one immediately following it.\n\n"
            "### Core Concept\nRelative comparison (Descending).\n\n"
            "### Detailed Logic\n1. Iterate through digits.\n"
            "2. If `digit[i] > digit[i+1]`, increment the counter.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The total count of decreasing pairs).\n\n"
            "### Example Walkthrough\n**Input:** 5426 -> (5>4) and (4>2). **Result: 2**"
        ),
        (
            "Problem 132: Digit Rotation Equality",
            "### Problem Overview\nRotate the digits of the number (e.g., move the last digit to the front) and check if the number remains identical to the original.\n\n"
            "### Core Concept\nCircular shifting and equality testing.\n\n"
            "### Detailed Logic\n1. Convert the number to a string or list.\n"
            "2. Shift the digits by one position (last becomes first).\n"
            "3. Compare the rotated version with the original.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the rotated number equals the original, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1212 -> Rotate: 2121. (False). **Input:** 555 -> Rotate: 555. (True)."
        ),
        (
            "Problem 133: Digit Swap Maximum",
            "### Problem Overview\nFind the largest possible number you can create by swapping exactly two digits once.\n\n"
            "### Core Concept\nGreedy selection and optimization.\n\n"
            "### Detailed Logic\n1. Identify the largest digit and its last occurrence.\n"
            "2. Swap it with the leftmost digit that is smaller than it.\n"
            "3. If the number is already at its maximum, perform no swap.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The maximum number achievable after one swap).\n\n"
            "### Example Walkthrough\n**Input:** 2736 -> Swap 2 and 7 -> 7236. **Result: 7236**"
        ),
        (
            "Problem 134: Digit Swap Minimum",
            "### Problem Overview\nFind the smallest possible number you can create by swapping exactly two digits once.\n\n"
            "### Core Concept\nMinimization logic and constraint handling (e.g., leading zeros).\n\n"
            "### Detailed Logic\n1. Identify the smallest digit.\n"
            "2. Swap it with the leftmost digit that is larger than it.\n"
            "3. Ensure that you do not swap a 0 into the first position if the number has multiple digits.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The minimum number achievable after one swap).\n\n"
            "### Example Walkthrough\n**Input:** 4352 -> Swap 4 and 2 -> 2354. **Result: 2354**"
        ),
        (
            "Problem 135: Remove One Digit Largest Number",
            "### Problem Overview\nDelete exactly one digit from the number such that the remaining digits form the largest possible number.\n\n"
            "### Core Concept\nPeak-removal strategy.\n\n"
            "### Detailed Logic\n1. Traverse the digits from left to right.\n"
            "2. Remove the first digit that is smaller than the digit to its right.\n"
            "3. If no such digit is found, remove the last digit.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The largest resulting number).\n\n"
            "### Example Walkthrough\n**Input:** 4352 -> Remove 3 -> 452. **Result: 452**"
        ),
        (
            "Problem 136: Remove One Digit Smallest Number",
            "### Problem Overview\nDelete exactly one digit from the number such that the remaining digits form the smallest possible number.\n\n"
            "### Core Concept\nValley-removal strategy.\n\n"
            "### Detailed Logic\n1. Traverse from left to right.\n"
            "2. Remove the first digit that is larger than the digit to its right.\n"
            "3. If the sequence is non-decreasing, remove the last digit.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The smallest resulting number).\n\n"
            "### Example Walkthrough\n**Input:** 1524 -> Remove 5 -> 124. **Result: 124**"
        ),
        (
            "Problem 137: Majority Digit Check",
            "### Problem Overview\nDetermine if any single digit appears more than $N/2$ times, where $N$ is the total number of digits.\n\n"
            "### Core Concept\nBoyer-Moore Voting Algorithm or Frequency Counting.\n\n"
            "### Detailed Logic\n1. Count the frequency of all digits.\n"
            "2. Check if the highest frequency is greater than half the length of the number.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a majority digit exists, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1211 -> Length 4. '1' appears 3 times. $3 > (4/2)$. **Result: True**"
        ),
        (
            "Problem 138: Consecutive Digit Gap",
            "### Problem Overview\nCalculate the difference between all neighboring digits and find the maximum gap.\n\n"
            "### Core Concept\nAbsolute difference and maximum tracking.\n\n"
            "### Detailed Logic\n1. Iterate through the number comparing pairs: `abs(digit[i] - digit[i+1])`.\n"
            "2. Keep track of the highest difference found.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The largest gap found).\n\n"
            "### Example Walkthrough\n**Input:** 182 -> Gaps: $|1-8|=7$, $|8-2|=6$. Max is 7. **Result: 7**"
        ),
        (
            "Problem 139: Digit Pair Sum Equal Target",
            "### Problem Overview\nCheck if any two digits within the number add up to a specific target value provided in the input.\n\n"
            "### Core Concept\nTwo-pointer approach or Set-based complement lookup.\n\n"
            "### Detailed Logic\n1. Store digits in a set.\n"
            "2. For each digit $D$, check if $(Target - D)$ exists in the set.\n"
            "3. Return True if a pair is found.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a pair exists, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1234, Target 7 -> Pair (3,4) adds to 7. **Result: True**"
        ),
        (
            "Problem 140: Reverse Half Equality",
            "### Problem Overview\nDivide the number into two halves. Check if the first half is the exact reverse of the second half.\n\n"
            "### Core Concept\nString slicing and reversal comparison.\n\n"
            "### Detailed Logic\n1. Split the number into two equal strings.\n"
            "2. Reverse the second half string.\n"
            "3. Compare it to the first half string.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the halves are mirror images, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1221 -> Half1: 12, Half2: 21. Reverse Half2: 12. **Result: True**"
        ),
        (
            "Problem 141: Digit Balance Point",
            "### Problem Overview\nIdentify an index (balance point) where the sum of digits to the left equals the sum of digits to the right.\n\n"
            "### Core Concept\nEquilibrium point logic.\n\n"
            "### Detailed Logic\n1. Calculate the total sum of all digits.\n"
            "2. Iterate through digits, maintaining a `left_sum`.\n"
            "3. For each digit, `right_sum = Total - left_sum - current_digit`.\n"
            "4. If `left_sum == right_sum`, return the index.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The index of the balance point) or `-1` if none exists.\n\n"
            "### Example Walkthrough\n**Input:** 12312 -> Sums: (1+2) = 3 and (1+2) = 3. Balance point is '3' at index 2. **Result: 2**"
        ),
        (
            "Problem 142: Digit Peak Pattern",
            "### Problem Overview\nCheck if there is at least one digit in the number that is strictly greater than both its left and right neighbors.\n\n"
            "### Core Concept\nLocal maxima identification in a numeric sequence.\n\n"
            "### Detailed Logic\n1. Iterate through the digits from index 1 to $len-2$.\n"
            "2. For each digit, check if `digit[i-1] < digit[i]` AND `digit[i] > digit[i+1]`.\n"
            "3. Return True if such a 'peak' is found.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a peak exists, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 132 -> 3 is greater than 1 and 2. **Result: True**"
        ),
        (
            "Problem 143: Digit Valley Pattern",
            "### Problem Overview\nCheck if there is a digit that is strictly smaller than both its neighbors.\n\n"
            "### Core Concept\nLocal minima identification.\n\n"
            "### Detailed Logic\n1. Iterate from the second digit to the second-to-last digit.\n"
            "2. Check if `digit[i-1] > digit[i]` AND `digit[i] < digit[i+1]`.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a valley exists, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 524 -> 2 is smaller than 5 and 4. **Result: True**"
        ),
        (
            "Problem 144: Circular Digit Match",
            "### Problem Overview\nCompare the first and last digits of a number and verify if they match or satisfy a specific equality rule.\n\n"
            "### Core Concept\nBoundary element comparison.\n\n"
            "### Detailed Logic\n1. Extract the first digit (using division or string indexing).\n"
            "2. Extract the last digit (using `% 10`).\n"
            "3. Compare the two values for equality.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the first and last digits are equal, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 7127 -> First is 7, Last is 7. **Result: True**"
        ),
        (
            "Problem 145: Repeated Pair Pattern",
            "### Problem Overview\nCheck whether the same pair of digits appears consecutively (one after the other) in the number.\n\n"
            "### Core Concept\nSubstring or sub-sequence matching.\n\n"
            "### Detailed Logic\n1. Look at pairs of digits: `(digit[i], digit[i+1])`.\n"
            "2. Compare with the next pair: `(digit[i+2], digit[i+3])`.\n"
            "3. Return True if the two pairs are identical.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a repeated consecutive pair exists).\n\n"
            "### Example Walkthrough\n**Input:** 1212 -> Pair '12' is followed by '12'. **Result: True**"
        ),
        (
            "Problem 146: Digit Group Equality",
            "### Problem Overview\nDivide the digits into groups of a fixed size and verify if the sum of digits in each group is identical.\n\n"
            "### Core Concept\nChunking and aggregate comparison.\n\n"
            "### Detailed Logic\n1. Split the digits into groups (e.g., pairs).\n"
            "2. Calculate the sum of each group.\n"
            "3. If all sums are equal, return True.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if all group sums match).\n\n"
            "### Example Walkthrough\n**Input:** 1524 -> Groups: (1,5) sum=6, (2,4) sum=6. **Result: True**"
        ),
        (
            "Problem 147: Digit Distance Rule",
            "### Problem Overview\nCheck whether identical digits in the number always appear at a consistent distance (gap) from each other.\n\n"
            "### Core Concept\nInterval consistency validation.\n\n"
            "### Detailed Logic\n1. Track the indices of every digit occurrence.\n"
            "2. For any digit that appears multiple times, calculate the distance between its positions.\n"
            "3. If distances for all repeating digits are the same, return True.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if distances are consistent, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1212 -> '1's are 2 apart, '2's are 2 apart. **Result: True**"
        ),
        (
            "Problem 148: Mirror Position Digits Equal",
            "### Problem Overview\nCompare digits from the start and end simultaneously (symmetrically) and ensure every pair matches.\n\n"
            "### Core Concept\nPalindrome-style element-wise comparison.\n\n"
            "### Detailed Logic\n1. Use two pointers: one at the start ($i=0$) and one at the end ($j=len-1$).\n"
            "2. While $i < j$, check if `digit[i] == digit[j]`.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if all symmetric pairs match, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 1221 -> 1=1, 2=2. **Result: True**"
        ),
        (
            "Problem 149: Longest Increasing Digit Segment",
            "### Problem Overview\nFind the length of the longest continuous sequence of digits where each digit is greater than the previous one.\n\n"
            "### Core Concept\nDynamic count tracking within a single pass.\n\n"
            "### Detailed Logic\n1. Initialize `max_len = 1` and `current_len = 1`.\n"
            "2. Iterate through digits: if `digit[i] > digit[i-1]`, increment `current_len`.\n"
            "3. Else, reset `current_len = 1`.\n"
            "4. Update `max_len` at each step.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The length of the longest increasing segment).\n\n"
            "### Example Walkthrough\n**Input:** 12312 -> Segments are '123' and '12'. Max length is 3. **Result: 3**"
        ),
        (
            "Problem 150: Longest Decreasing Digit Segment",
            "### Problem Overview\nFind the length of the longest continuous sequence of digits where each digit is smaller than the previous one.\n\n"
            "### Core Concept\nDynamic count tracking (Descending).\n\n"
            "### Detailed Logic\n1. Similar to the increasing segment logic, but check for `digit[i] < digit[i-1]`.\n"
            "2. Track the highest length encountered.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The length of the longest decreasing segment).\n\n"
            "### Example Walkthrough\n**Input:** 54321 -> Entire number is decreasing. **Result: 5**"
        ),
        (
            "Problem 151: Digit Pattern Stability",
            "### Problem Overview\nCheck whether the difference between consecutive digits follows a repeating pattern (e.g., +1, -1, +1, -1).\n\n"
            "### Core Concept\nDelta sequence analysis.\n\n"
            "### Detailed Logic\n1. Calculate the sequence of differences: `diff[i] = digit[i+1] - digit[i]`.\n"
            "2. Check if this sequence of differences repeats itself.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if a stable repeating difference pattern is found).\n\n"
            "### Example Walkthrough\n**Input:** 12121 -> Differences: +1, -1, +1, -1. **Result: True**"
        ),
        (
            "Problem 152: Check Even or Odd Using Bitwise",
            "### Problem Overview\nDetermine if a number is even or odd using the bitwise AND operator instead of modulus.\n\n"
            "### Core Concept\nBinary parity check. In binary, even numbers always end in `0` and odd numbers always end in `1`.\n\n"
            "### Detailed Logic\n1. Perform the operation `(n & 1)`.\n"
            "2. If the result is `0`, the number is even.\n"
            "3. If the result is `1`, the number is odd.\n\n"
            "### Test Case Expectation\n- **Returns:** String (`'Even'` or `'Odd'`).\n\n"
            "### Example Walkthrough\n**Input:** 5 (Binary `101`) -> `101 & 001 = 1`. **Result: 'Odd'**"
        ),
        (
            "Problem 153: Extract Last Bit",
            "### Problem Overview\nFind the value of the least significant bit (LSB) of a given number.\n\n"
            "### Core Concept\nBit masking to isolate the $2^0$ position.\n\n"
            "### Detailed Logic\n1. Use the expression `n & 1` to mask all bits except the last one.\n"
            "2. The result will be either `0` or `1`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (`0` or `1`).\n\n"
            "### Example Walkthrough\n**Input:** 12 (Binary `1100`) -> `1100 & 0001 = 0`. **Result: 0**"
        ),
        (
            "Problem 154: Check if Bit is Set",
            "### Problem Overview\nGiven a number $N$ and a position $k$, determine if the bit at that position is `1`.\n\n"
            "### Core Concept\nBit shifting and masking.\n\n"
            "### Detailed Logic\n1. Shift the number $1$ to the left by $k$ positions: `mask = 1 << k`.\n"
            "2. Perform `n & mask`.\n"
            "3. If the result is not `0`, the bit is set.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the bit is `1`, `False` if `0`).\n\n"
            "### Example Walkthrough\n**Input:** N=5 (Binary `101`), k=2 -> `1 << 2` is `100`. `101 & 100 = 100` (Non-zero). **Result: True**"
        ),
        (
            "Problem 155: Set a Bit",
            "### Problem Overview\nModify a number so that the bit at a specific position $k$ becomes `1`.\n\n"
            "### Core Concept\nBitwise OR operation to force a bit to `1`.\n\n"
            "### Detailed Logic\n1. Create a mask: `mask = 1 << k`.\n"
            "2. Perform `n | mask`.\n"
            "3. The resulting number will have the $k$-th bit as `1` regardless of its previous state.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The updated number).\n\n"
            "### Example Walkthrough\n**Input:** N=8 (Binary `1000`), k=1 -> `8 | (1 << 1)` -> `1000 | 0010 = 1010`. **Result: 10**"
        ),
        (
            "Problem 156: Clear a Bit",
            "### Problem Overview\nChange a specific bit at position $k$ to `0` while leaving other bits unchanged.\n\n"
            "### Core Concept\nBitwise AND with a negated mask.\n\n"
            "### Detailed Logic\n1. Create a mask with `1` at position $k$: `1 << k`.\n"
            "2. Invert the mask (NOT): `~(1 << k)` (This creates `0` at $k$ and `1` everywhere else).\n"
            "3. Perform `n & mask`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The updated number).\n\n"
            "### Example Walkthrough\n**Input:** N=7 (Binary `111`), k=1 -> `7 & ~(1 << 1)` -> `111 & 101 = 101`. **Result: 5**"
        ),
        (
            "Problem 157: Toggle a Bit",
            "### Problem Overview\nFlip the value of a bit at position $k$ (if `0` becomes `1`, if `1` becomes `0`).\n\n"
            "### Core Concept\nBitwise XOR operation.\n\n"
            "### Detailed Logic\n1. Create a mask: `mask = 1 << k`.\n"
            "2. Perform `n ^ mask`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The updated number).\n\n"
            "### Example Walkthrough\n**Input:** N=6 (Binary `110`), k=0 -> `110 ^ 001 = 111`. **Result: 7**"
        ),
        (
            "Problem 158: Count Set Bits",
            "### Problem Overview\nCalculate the total number of bits equal to `1` in the binary representation of a number.\n\n"
            "### Core Concept\nPopulation count (Hamming weight).\n\n"
            "### Detailed Logic\n1. Use a loop: while $n > 0$, increment counter if `n & 1` is `1`.\n"
            "2. Shift $n$ right by one: `n >>= 1`.\n"
            "3. Alternatively, use Brian Kernighan’s algorithm: `n = n & (n - 1)` to clear bits one by one.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (Total count of set bits).\n\n"
            "### Example Walkthrough\n**Input:** 7 (Binary `111`) -> Count = 3. **Result: 3**"
        ),
        (
            "Problem 159: Check Power of Two",
            "### Problem Overview\nDetermine if a number is a power of two using bitwise logic.\n\n"
            "### Core Concept\nPowers of two (2, 4, 8, 16...) have exactly one bit set in binary.\n\n"
            "### Detailed Logic\n1. If $n \leq 0$, return False.\n"
            "2. Use the property: `(n & (n - 1)) == 0`.\n"
            "3. If true, the number has exactly one bit set.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if power of two, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 8 (Binary `1000`) -> `8 & 7` (1000 & 0111) = 0. **Result: True**"
        ),
        (
            "Problem 160: Remove Lowest Set Bit",
            "### Problem Overview\nClear the rightmost bit that is set to `1` and return the resulting value.\n\n"
            "### Core Concept\nBitwise subtraction property.\n\n"
            "### Detailed Logic\n1. Perform `n & (n - 1)`.\n"
            "2. This operation effectively flips the rightmost `1` and all `0`s to its right.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The new value after removing the LSB).\n\n"
            "### Example Walkthrough\n**Input:** 12 (Binary `1100`) -> `1100 & 1011 = 1000`. **Result: 8**"
        ),
        (
            "Problem 161: Find Rightmost Set Bit Position",
            "### Problem Overview\nIdentify the position (1-indexed) of the first bit equal to `1` starting from the right.\n\n"
            "### Core Concept\nBinary scanning or logarithmic calculation.\n\n"
            "### Detailed Logic\n1. Isolate the rightmost bit: `isolated = n & -n`.\n"
            "2. Calculate the position using $log_2(isolated) + 1$ or a loop.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (Position index).\n\n"
            "### Example Walkthrough\n**Input:** 10 (Binary `1010`) -> Rightmost set bit is at position 2. **Result: 2**"
        ),
        (
            "Problem 162: Check Opposite Parity",
            "### Problem Overview\nGiven two numbers, determine whether one is even and the other is odd using bitwise logic.\n\n"
            "### Core Concept\nBitwise XOR of the last bits. If two numbers have different last bits, their parity is opposite.\n\n"
            "### Detailed Logic\n1. Extract the last bit of both: `(a & 1)` and `(b & 1)`.\n"
            "2. Compare them using XOR: `(a & 1) ^ (b & 1)`.\n"
            "3. If the result is 1, they have opposite parity.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if one is even and one is odd, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** a=4, b=5 -> `(0 ^ 1) = 1`. **Result: True**"
        ),
        ( "### Problem Overview\nGiven an integer $N$ and a position $k$, determine whether the bit at that specific position is 'Clear' (0).\n\n"
            "### Core Concept\nBitwise masking using the NOT operator. A bit is clear if its value in binary is 0.\n\n"
            "### Detailed Logic\n1. Create a mask by shifting 1 to the left by $k$ positions: `mask = 1 << k`.\n"
            "2. Perform a bitwise AND between $N$ and the mask.\n"
            "3. If the result is exactly 0, the bit at position $k$ is clear.\n"
            "4. Alternatively, shift $N$ right by $k$ and check if the last bit is 0: `(n >> k) & 1 == 0`.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if the bit is 0, `False` if the bit is 1).\n\n"
            "### Example Walkthrough\n**Input:** N=10 (Binary `1010`), k=2\n- Binary at index 2 is `0`.\n- `10 & (1 << 2)` -> `1010 & 0100` = `0000`.\n**Result: True**"
                 ),
        (
            "Problem 164: Bitwise XOR Difference",
            "### Problem Overview\nCompute the XOR of two numbers to identify which specific bit positions are different.\n\n"
            "### Core Concept\nXOR outputs `1` only when the bits at a position are different.\n\n"
            "### Detailed Logic\n1. Calculate `result = a ^ b`.\n"
            "2. The set bits in the result represent the differing positions.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The result of `a ^ b`).\n\n"
            "### Example Walkthrough\n**Input:** 10 (1010), 12 (1100) -> `1010 ^ 1100 = 0110` (Decimal 6). **Result: 6**"
        ),
        (
            "Problem 165: Count Bit Changes Between Two Numbers",
            "### Problem Overview\nDetermine how many bits must be flipped to convert one number into another. Also known as Hamming Distance.\n\n"
            "### Core Concept\nXOR to find differences, then count the set bits.\n\n"
            "### Detailed Logic\n1. Calculate `diff = a ^ b`.\n"
            "2. Count the number of set bits (`1`s) in `diff`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (Total count of differing bits).\n\n"
            "### Example Walkthrough\n**Input:** 7 (111), 10 (1010) -> XOR is 1101. Three bits are set. **Result: 3**"
        ),
        (
            "Problem 166: Check Alternating Bits",
            "### Problem Overview\nVerify if the binary representation of a number consists of alternating `0`s and `1`s (e.g., `1010`).\n\n"
            "### Core Concept\nShifted XOR property. If bits alternate, `n ^ (n >> 1)` will result in all bits being `1`.\n\n"
            "### Detailed Logic\n1. Let `x = n ^ (n >> 1)`.\n"
            "2. Check if `x` is a number where all bits are set (i.e., `x + 1` is a power of 2).\n"
            "3. Verify `(x & (x + 1)) == 0`.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if bits alternate, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 5 (101) -> `101 ^ 010 = 111`. `111 & 1000 = 0`. **Result: True**"
        ),
        (
            "Problem 167: Reverse Binary Bits",
            "### Problem Overview\nReverse the order of bits in the binary representation of a 32-bit integer.\n\n"
            "### Core Concept\nBit manipulation with shifting and accumulation.\n\n"
            "### Detailed Logic\n1. Initialize `result = 0`.\n"
            "2. Loop 32 times: Shift `result` left, add `n & 1`, then shift `n` right.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The value after bit reversal).\n\n"
            "### Example Walkthrough\n**Input:** 13 (1101) -> Reversed (within 4 bits) is 1011 (11). **Result: 11**"
        ),
        (
            "Problem 168: Binary Palindrome",
            "### Problem Overview\nCheck whether the binary representation of a number reads the same forward and backward.\n\n"
            "### Core Concept\nReverse bits and compare to original.\n\n"
            "### Detailed Logic\n1. Construct the reversed binary number using bit shifts.\n"
            "2. Compare the reversed version with the original `n`.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if binary is palindromic, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 9 (1001) -> Reversed: 1001. **Result: True**"
        ),
        (
            "Problem 169: Multiply Using Left Shift",
            "### Problem Overview\nMultiply a number $N$ by $2^k$ using the left shift operator.\n\n"
            "### Core Concept\nEach left shift `<< 1` doubles the number.\n\n"
            "### Detailed Logic\n1. Perform `n << k`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The result of $n \times 2^k$).\n\n"
            "### Example Walkthrough\n**Input:** n=5, k=2 -> `5 << 2` is $5 \times 4 = 20$. **Result: 20**"
        ),
        (
            "Problem 170: Divide Using Right Shift",
            "### Problem Overview\nDivide a number $N$ by $2^k$ (integer division) using the right shift operator.\n\n"
            "### Core Concept\nEach right shift `>> 1` halves the number.\n\n"
            "### Detailed Logic\n1. Perform `n >> k`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The result of $n // 2^k$).\n\n"
            "### Example Walkthrough\n**Input:** n=20, k=2 -> `20 >> 2` is $20 // 4 = 5$. **Result: 5**"
        ),
        (
            "Problem 171: Check Only One Bit Set",
            "### Problem Overview\nDetermine if the binary form of a number contains exactly one `1` bit.\n\n"
            "### Core Concept\nThis is identical to checking if a number is a power of 2.\n\n"
            "### Detailed Logic\n1. Check `n > 0`.\n"
            "2. Verify `(n & (n - 1)) == 0`.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if exactly one bit is set).\n\n"
            "### Example Walkthrough\n**Input:** 16 (10000) -> Only one bit set. **Result: True**"
        ),
        (
            "Problem 172: Turn Off Rightmost Set Bit",
            "### Problem Overview\nModify the number by turning off (setting to 0) only the rightmost bit that is currently 1.\n\n"
            "### Core Concept\nBitwise subtraction property. Subtraction by 1 flips all bits from the right up to the first set bit.\n\n"
            "### Detailed Logic\n1. Perform the operation `n & (n - 1)`.\n"
            "2. This preserves all bits to the left of the rightmost set bit and clears everything else.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The updated value).\n\n"
            "### Example Walkthrough\n**Input:** 12 (1100) -> `12 & 11` (1100 & 1011) = 1000. **Result: 8**"
        ),
        (
            "Problem 173: Isolate Rightmost Set Bit",
            "### Problem Overview\nExtract only the lowest set bit from the number and clear all other bits to 0.\n\n"
            "### Core Concept\nTwo's complement property. `-n` is equal to `(~n + 1)`.\n\n"
            "### Detailed Logic\n1. Perform the operation `n & -n`.\n"
            "2. The result will be a power of two representing the position of the LSB.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The value of the isolated bit).\n\n"
            "### Example Walkthrough\n**Input:** 20 (10100) -> `20 & -20` = 4 (00100). **Result: 4**"
        ),
        (
            "Problem 174: Check Consecutive Set Bits",
            "### Problem Overview\nCheck whether the binary representation contains at least two consecutive bits with the value 1.\n\n"
            "### Core Concept\nBitwise shift and AND comparison.\n\n"
            "### Detailed Logic\n1. Perform `n & (n << 1)`.\n"
            "2. If the result is not 0, it means at least one pair of 1s was aligned.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if consecutive 1s exist, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 3 (11) -> `3 & (3 << 1)` = `011 & 110` = 010 (Non-zero). **Result: True**"
        ),
        (
            "Problem 175: Count Trailing Zeros in Binary",
            "### Problem Overview\nCount how many zeros appear at the end of the binary representation before reaching the first 1.\n\n"
            "### Core Concept\nFinding the index of the first set bit.\n\n"
            "### Detailed Logic\n1. Isolate the rightmost set bit: `lowbit = n & -n`.\n"
            "2. Count how many times you can shift `lowbit` right before it becomes 0, or use `(lowbit - 1).bit_count()`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (Count of trailing zeros).\n\n"
            "### Example Walkthrough\n**Input:** 8 (1000) -> Three trailing zeros. **Result: 3**"
        ),
        (
            "Problem 176: Binary Length of Number",
            "### Problem Overview\nDetermine the minimum number of bits required to represent an integer in binary.\n\n"
            "### Core Concept\nMost Significant Bit (MSB) position.\n\n"
            "### Detailed Logic\n1. Use the built-in `n.bit_length()` in Python.\n"
            "2. Or, repeatedly shift right until the number becomes 0, counting the steps.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (Number of bits).\n\n"
            "### Example Walkthrough\n**Input:** 5 (101) -> Length is 3 bits. **Result: 3**"
        ),
        (
            "Problem 177: Toggle All Bits up to MSB",
            "### Problem Overview\nInvert all bits from the LSB up to the highest set bit (MSB).\n\n"
            "### Core Concept\nCreating a full bit-mask.\n\n"
            "### Detailed Logic\n1. Find the bit length $k$ of the number.\n"
            "2. Create a mask of $k$ ones: `mask = (1 << k) - 1`.\n"
            "3. Return `n ^ mask`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The value after inversion).\n\n"
            "### Example Walkthrough\n**Input:** 10 (1010) -> Mask is 1111 (15). `10 ^ 15 = 5` (0101). **Result: 5**"
        ),
        (
            "Problem 178: Check Bit Symmetry",
            "### Problem Overview\nDetermine if the binary pattern is symmetric (a binary palindrome).\n\n"
            "### Core Concept\nBit reversal and comparison.\n\n"
            "### Detailed Logic\n1. Find the bit length of $N$.\n"
            "2. Reverse the bits manually within that specific length.\n"
            "3. Compare the reversed value to the original $N$.\n\n"
            "### Test Case Expectation\n- **Returns:** Boolean (`True` if symmetric, `False` otherwise).\n\n"
            "### Example Walkthrough\n**Input:** 5 (101) -> Symmetric. **Result: True** | **Input:** 6 (110) -> Not symmetric. **Result: False**"
        ),
        (
            "Problem 179: Binary Gap",
            "### Problem Overview\nFind the longest distance between two consecutive set bits (1s) in the binary representation.\n\n"
            "### Core Concept\nDistance tracking during bit traversal.\n\n"
            "### Detailed Logic\n1. Track the index of the last seen 1.\n"
            "2. When the next 1 is found, calculate `current_index - last_index`.\n"
            "3. Update `max_gap` if this distance is larger.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The largest distance).\n\n"
            "### Example Walkthrough\n**Input:** 9 (1001) -> Gap between index 0 and 3 is 3. **Result: 3**"
        ),
        (
            "Problem 180: Rotate Bits Left",
            "### Problem Overview\nPerform a circular left shift where the MSB wraps around to the LSB position (assuming a fixed bit-width like 8 or 32).\n\n"
            "### Core Concept\nCircular shifting logic.\n\n"
            "### Detailed Logic\n1. Let $k$ be the rotation amount and $W$ be the bit width.\n"
            "2. `result = ((n << k) | (n >> (W - k))) & ((1 << W) - 1)`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The rotated value).\n\n"
            "### Example Walkthrough\n**Input:** n=128 (10000000), k=1 (8-bit) -> Result: 1 (00000001). **Result: 1**"
        ),
        (
            "Problem 181: Rotate Bits Right",
            "### Problem Overview\nPerform a circular right shift where the LSB wraps around to the MSB position.\n\n"
            "### Core Concept\nCircular shifting (Right).\n\n"
            "### Detailed Logic\n1. Let $k$ be the rotation amount and $W$ be the bit width.\n"
            "2. `result = ((n >> k) | (n << (W - k))) & ((1 << W) - 1)`.\n\n"
            "### Test Case Expectation\n- **Returns:** Integer (The rotated value).\n\n"
            "### Example Walkthrough\n**Input:** n=1 (00000001), k=1 (8-bit) -> Result: 128 (10000000). **Result: 128**"
        )]
        start_date = datetime(2026, 3, 24)

        for index, (title, content) in enumerate(challenges):
            # Calculate date sequentially
            date_obj = start_date + timedelta(days=index)
            date_str = date_obj.strftime("%Y-%m-%d")

            cursor.execute(
                """
                INSERT INTO questions (title, date, content, solution)
                VALUES (%s, %s, %s, %s)
                """,
                (title, date_str, content, "")
            )

        conn.commit()
        cursor.close()
        conn.close()

        print(f"✅ Success: {len(challenges)} problems inserted starting from {start_date.strftime('%Y-%m-%d')}.")

    except Exception as e:
        print(f"❌ Error:", e)

if __name__ == "__main__":
    setup_professional_curriculum()
    




        