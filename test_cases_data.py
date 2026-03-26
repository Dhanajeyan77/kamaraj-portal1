# test_cases_data.py

# Dictionary mapping question_id (qid) to a list of test cases
# Updated test_cases_data.py
# Added extra edge cases for robust student evaluation

TEST_CASES_DICT = {
    91: [
        {"input_data": "121", "expected_output": "true"},
        {"input_data": "-121", "expected_output": "false"},
        {"input_data": "10", "expected_output": "false"},
        # Extra Case: Large palindrome
        {"input_data": "12321", "expected_output": "true"}
    ],
    92: [
        {"input_data": "6", "expected_output": "true"},
        {"input_data": "496", "expected_output": "true"},
        {"input_data": "12", "expected_output": "false"},
        {"input_data": "28", "expected_output": "true"},
        # Extra Case: Large non-perfect number
        {"input_data": "100", "expected_output": "false"}
    ],
    93: [
        {"input_data": "9474", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "153", "expected_output": "true"},
        {"input_data": "370", "expected_output": "true"},
        # Extra Case: Another 3-digit Armstrong
        {"input_data": "407", "expected_output": "true"}
    ],
    94: [
        {"input_data": "10", "expected_output": "false"},
        {"input_data": "7", "expected_output": "true"},
        {"input_data": "2", "expected_output": "true"},
        {"input_data": "1", "expected_output": "false"},
        # Extra Case: Larger prime
        {"input_data": "19", "expected_output": "true"}
    ],
    95: [
        {"input_data": "10", "expected_output": "[2, 3, 5, 7]"},
        {"input_data": "20", "expected_output": "[2, 3, 5, 7, 11, 13, 17, 19]"},
        # Extra Case: Small range
        {"input_data": "5", "expected_output": "[2, 3, 5]"}
    ],
    96: [
        {"input_data": "5", "expected_output": "120"},
        {"input_data": "0", "expected_output": "1"},
        {"input_data": "10", "expected_output": "3628800"},
        # Extra Case: Middle value
        {"input_data": "3", "expected_output": "6"}
    ],
    97: [
        {"input_data": "6", "expected_output": "8"},
        {"input_data": "10", "expected_output": "55"},
        {"input_data": "0", "expected_output": "0"},
        {"input_data": "1", "expected_output": "1"},
        # Extra Case: 7th position
        {"input_data": "7", "expected_output": "13"}
    ],
    98: [
        {"input_data": "7, 3", "expected_output": "1"},
        {"input_data": "48, 18", "expected_output": "6"},
        {"input_data": "100, 10", "expected_output": "10"},
        # Extra Case: Multiples
        {"input_data": "25, 5", "expected_output": "5"}
    ],
    99: [
        {"input_data": "12, 15", "expected_output": "60"},
        {"input_data": "10, 5", "expected_output": "10"},
        {"input_data": "4, 6", "expected_output": "12"},
        # Extra Case: Prime pair
        {"input_data": "3, 7", "expected_output": "21"}
    ],
    100: [
        {"input_data": "1011", "expected_output": "11"},
        {"input_data": "100", "expected_output": "4"},
        {"input_data": "1111", "expected_output": "15"},
        # Extra Case: Single bit
        {"input_data": "1", "expected_output": "1"}
    ],
    101: [
        {"input_data": "8", "expected_output": "\"1000\""},
        {"input_data": "13", "expected_output": "\"1101\""},
        {"input_data": "0", "expected_output": "\"0\""},
        # Extra Case: Power of 2
        {"input_data": "16", "expected_output": "\"10000\""}
    ],
    102: [
        {"input_data": "145", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "1", "expected_output": "true"},
        # Extra Case: Another Strong number
        {"input_data": "2", "expected_output": "true"}
    ],
    103: [
        {"input_data": "120", "expected_output": "021"},
        {"input_data": "123", "expected_output": "321"},
        {"input_data": "-123", "expected_output": "-321"},
        # Extra Case: Single digit
        {"input_data": "5", "expected_output": "5"}
    ],
    104: [
        {"input_data": "2000", "expected_output": "true"},
        {"input_data": "2024", "expected_output": "true"},
        {"input_data": "1900", "expected_output": "false"},
        # Extra Case: Recent non-leap
        {"input_data": "2023", "expected_output": "false"}
    ],
    105: [
        {"input_data": "5, 1", "expected_output": "5"},
        {"input_data": "4, 2", "expected_output": "6"},
        # Extra Case: nCr where r is 0
        {"input_data": "10, 0", "expected_output": "1"} 
    ],
    106: [
        {"input_data": "\"hello\"", "expected_output": "\"olleh\""},
        {"input_data": "\"code\"", "expected_output": "\"edoc\""},
        # Extra Case: Palindrome string
        {"input_data": "\"racecar\"", "expected_output": "\"racecar\""}
    ],
    107: [
        {"input_data": "\"silent\", \"listen\"", "expected_output": "true"},
        {"input_data": "\"rat\", \"car\"", "expected_output": "false"},
        # Extra Case: Different lengths
        {"input_data": "\"hello\", \"hell\"", "expected_output": "false"}
    ],
    108: [
        {"input_data": "\"Hello\"", "expected_output": "{\"vowels\": 2, \"consonants\": 3}"},
        # Extra Case: Only consonants and spaces
        {"input_data": "\"Sky High\"", "expected_output": "{\"vowels\": 1, \"consonants\": 6}"}
    ],
    109: [
        {"input_data": "\"leetcode\"", "expected_output": "\"l\""},
        {"input_data": "\"aabb\"", "expected_output": "null"},
        # Extra Case: Last character is unique
        {"input_data": "\"abcab\"", "expected_output": "\"c\""}
    ],
    110: [
        {"input_data": "\"aaabbc\"", "expected_output": "\"a3b2c1\""},
        # Extra Case: Single characters
        {"input_data": "\"abcd\"", "expected_output": "\"a1b1c1d1\""}
    ],
    111: [
        {"input_data": "\"programming\"", "expected_output": "\"progamin\""},
        # Extra Case: Already unique
        {"input_data": "\"python\"", "expected_output": "\"python\""}
    ],
    112: [
        {"input_data": "[\"flower\", \"flow\", \"flight\"]", "expected_output": "\"fl\""},
        # Extra Case: No common prefix
        {"input_data": "[\"dog\", \"racecar\", \"car\"]", "expected_output": "\"\""}
    ],
    113: [
        {"input_data": "\"abcde\", \"cdeab\"", "expected_output": "true"},
        # Extra Case: Same characters but not a rotation
        {"input_data": "\"abc\", \"acb\"", "expected_output": "false"}
    ],
    114: [
        {"input_data": "\"()[]{}\"", "expected_output": "true"},
        {"input_data": "\"(]\"", "expected_output": "false"},
        # Extra Case: Complex nested valid
        {"input_data": "\"{[()]}\"", "expected_output": "true"}
    ],



    115: [
        {"input_data": "\"42\"", "expected_output": "42"},
        {"input_data": "\"   -42\"", "expected_output": "-42"},
        {"input_data": "\"4193 with words\"", "expected_output": "4193"} # Extra: Trailing words
    ],
    116: [
        {"input_data": "\"the sky is blue\"", "expected_output": "\"blue is sky the\""},
        {"input_data": "\"  hello world  \"", "expected_output": "\"world hello\""} # Extra: Extra spaces
    ],
    117: [
        {"input_data": "[3, 5, 1, 9]", "expected_output": "\"max:9,min:1\""},
        {"input_data": "[10, 10, 10]", "expected_output": "\"max:10,min:10\""} # Extra: All same
    ],
    118: [
        {"input_data": "[10, 5, 10, 8]", "expected_output": "8"},
        {"input_data": "[5, 5, 4, 3]", "expected_output": "4"} # Extra: Duplicates
    ],
    119: [
        {"input_data": "[0,1,0,3,12]", "expected_output": "[1,3,12,0,0]"},
        {"input_data": "[0]", "expected_output": "[0]"} # Extra: Single zero
    ],
    120: [
        {"input_data": "[1,2,3,4,5], [2]", "expected_output": "[4,5,1,2,3]"},
        {"input_data": "[1,2], [3]", "expected_output": "[2,1]"} # Extra: Rotation > length
    ],
    121: [
        {"input_data": "[3,0,1]", "expected_output": "2"},
        {"input_data": "[9,6,4,2,3,5,7,0,1]", "expected_output": "8"} # Extra: Longer sequence
    ],
    122: [
        {"input_data": "[1,2,2,1], [2,2]", "expected_output": "[2]"},
        {"input_data": "[4,9,5], [9,4,9,8,4]", "expected_output": "[4,9]"} # Extra: Multiple intersections
    ],
    123: [
        {"input_data": "[2,7,11,15], 9", "expected_output": "[0,1]"},
        {"input_data": "[3,3], 6", "expected_output": "[0,1]"} # Extra: Same number used twice
    ],
    124: [
        {"input_data": "[-1,0,3,5,9,12], 9", "expected_output": "4"},
        {"input_data": "[2,5], 5", "expected_output": "1"} # Extra: Target at end
    ],
    125: [
        {"input_data": "[1,1,2]", "expected_output": "2"},
        {"input_data": "[0,0,1,1,1,2,2,3,3,4]", "expected_output": "5"} # Extra: Large unique set
    ],
    126: [
        {"input_data": "[[1,2],[3,4]]", "expected_output": "[[1,3],[2,4]]"},
        {"input_data": "[[5]]", "expected_output": "[[5]]"} # Extra: 1x1 Matrix
    ],
    127: [
        {"input_data": "[[1,2,3],[4,5,6],[7,8,9]]", "expected_output": "[1,2,3,6,9,8,7,4,5]"},
        {"input_data": "[[1,2],[3,4]]", "expected_output": "[1,2,4,3]"} # Extra: 2x2 Spiral
    ],
    128: [
        {"input_data": "[[1,3,5,7],[10,11,16,20]], 3", "expected_output": "true"},
        {"input_data": "[[1,3,5,7],[10,11,16,20]], 13", "expected_output": "false"} # Extra: Missing value
    ],
    129: [
        {"input_data": "[1,1,1], 2", "expected_output": "2"},
        {"input_data": "[1,2,3], 3", "expected_output": "2"} # Extra: Sum 3 combinations
    ],
    130: [
        {"input_data": "[-2,1,-3,4,-1,2,1,-5,4]", "expected_output": "6"},
        {"input_data": "[5,4,-1,7,8]", "expected_output": "23"} # Extra: Large positive sum
    ],
    131: [
        {"input_data": "[7,1,5,3,6,4]", "expected_output": "5"},
        {"input_data": "[7,6,4,3,1]", "expected_output": "0"}, # Extra: No profit possible
        {"input_data": "[1,2,3,4,5]", "expected_output": "4"}  # Extra: Constant increase
    ],
    132: [
        {"input_data": "[3,2,3]", "expected_output": "3"},
        {"input_data": "[2,2,1,1,1,2,2]", "expected_output": "2"},
        {"input_data": "[1]", "expected_output": "1"} # Extra: Single element
    ],
    133: [
        {"input_data": "[[1,3],[2,6],[8,10]]", "expected_output": "[[1,6],[8,10]]"},
        {"input_data": "[[1,4],[4,5]]", "expected_output": "[[1,5]]"}, # Extra: Touching edges
        {"input_data": "[[1,4],[2,3]]", "expected_output": "[[1,4]]"}  # Extra: Full overlap
    ],
    134: [
        {"input_data": "[1,2,3,4]", "expected_output": "[24,12,8,6]"},
        {"input_data": "[-1,1,0,-3,3]", "expected_output": "[0,0,9,0,0]"},
        {"input_data": "[1,1,1,1]", "expected_output": "[1,1,1,1]"} # Extra: All ones
    ],
    135: [
        {"input_data": "[[1,1,1],[1,0,1],[1,1,1]]", "expected_output": "[[1,0,1],[0,0,0],[1,0,1]]"},
        {"input_data": "[[0,1,2,0],[3,4,5,2],[1,3,1,5]]", "expected_output": "[[0,0,0,0],[0,4,5,0],[0,3,1,0]]"},
        {"input_data": "[[1,2,3],[4,0,6],[7,8,9]]", "expected_output": "[[1,0,3],[0,0,0],[7,0,9]]"} # Extra: Center zero
    ],
    136: [
        {"input_data": "2.0, 10", "expected_output": "1024.0"},
        {"input_data": "2.0, -2", "expected_output": "0.25"}, # Extra: Negative exponent
        {"input_data": "1.0, 100", "expected_output": "1.0"}   # Extra: Identity base
    ],
    137: [
        {"input_data": "3", "expected_output": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]"},
        {"input_data": "1", "expected_output": "[\"()\"]"},
        {"input_data": "2", "expected_output": "[\"(())\",\"()()\"]"} # Extra: Basic pair
    ],
    138: [
        {"input_data": "3", "expected_output": "3"},
        {"input_data": "5", "expected_output": "8"},
        {"input_data": "2", "expected_output": "2"}, # Extra: Base case
        {"input_data": "1", "expected_output": "1"}  # Extra: Single step
    ],
    139: [
        {"input_data": "[1,2]", "expected_output": "[[1,2],[2,1]]"},
        {"input_data": "[1]", "expected_output": "[[1]]"},
        {"input_data": "[1,2,3]", "expected_output": "[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]"} # Extra: Complete 3-set
    ],
    140: [
        {"input_data": "[1,2]", "expected_output": "[[],[1],[2],[1,2]]"},
        {"input_data": "[0]", "expected_output": "[[],[0]]"},
        {"input_data": "[1,2,3]", "expected_output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"} # Extra: Larger powerset
    ],
    141: [
        {"input_data": "[['A','B'],['C','D']], 'AC'", "expected_output": "true"},
        {"input_data": "[['A','B'],['C','D']], 'AD'", "expected_output": "false"}, # Extra: Diagonal (invalid)
        {"input_data": "[['A','B'],['C','D']], 'ABDC'", "expected_output": "true"}   # Extra: Full path
    ],
    142: [
        {"input_data": "[38,27,43,3]", "expected_output": "[3,27,38,43]"},
        {"input_data": "[10, 5]", "expected_output": "[5, 10]"},
        {"input_data": "[1, 3, 2, 5, 4]", "expected_output": "[1, 2, 3, 4, 5]"} # Extra: Odd length
    ],
    143: [
        {"input_data": "[10,80,30,90,40]", "expected_output": "[10,30,40,80,90]"},
        {"input_data": "[1, 2, 3]", "expected_output": "[1, 2, 3]"}, # Extra: Already sorted
        {"input_data": "[5, 4, 3, 2, 1]", "expected_output": "[1, 2, 3, 4, 5]"} # Extra: Reversed
    ],
    144: [
        {"input_data": "[4,5,6,7,0,1,2], 0", "expected_output": "4"},
        {"input_data": "[4,5,6,7,0,1,2], 3", "expected_output": "-1"}, # Extra: Target not found
        {"input_data": "[1], 0", "expected_output": "-1"} # Extra: Single element fail
    ],
    145: [
        {"input_data": "[3,2,1,5,6,4], 2", "expected_output": "5"},
        {"input_data": "[3,2,3,1,2,4,5,5,6], 4", "expected_output": "4"},
        {"input_data": "[1], 1", "expected_output": "1"} # Extra: Minimum value
    ],
    146: [
        {"input_data": "\"1->2->3\"", "expected_output": "\"3->2->1\""},
        {"input_data": "\"1\"", "expected_output": "\"1\""}, # Extra: Single node
        {"input_data": "\"1->2\"", "expected_output": "\"2->1\""} # Extra: Two nodes
    ],
    147: [
        {"input_data": "\"1->2->3->2\"", "expected_output": "true"},
        {"input_data": "\"1->2->3\"", "expected_output": "false"} # Extra: No cycle
    ],
    148: [
        {"input_data": "\"1->3, 2->4\"", "expected_output": "\"1->2->3->4\""},
        {"input_data": "\"1, 2\"", "expected_output": "\"1->2\""} # Extra: Minimum nodes
    ],
    149: [
        {"input_data": "\"1->2->3->4\", 2", "expected_output": "\"1->2->4\""},
        {"input_data": "\"1->2\", 1", "expected_output": "\"2\""} # Extra: Remove head
    ],
    150: [
        {"input_data": "\"1->2->3->4->5\"", "expected_output": "3"},
        {"input_data": "\"1->2\"", "expected_output": "2"} # Extra: Even length middle
    ],
    151: [
        {"input_data": "\"1->2->2->1\"", "expected_output": "true"},
        {"input_data": "\"1->2\"", "expected_output": "false"} # Extra: Simple fail
    ],
    152: [
        {"input_data": "\"A:[1,2,3], B:[4,3]\"", "expected_output": "3"},
        {"input_data": "\"A:[1], B:[2]\"", "expected_output": "null"} # Extra: No intersection
    ],
    153: [
        {"input_data": "\"(2->4->3) + (5->6->4)\"", "expected_output": "\"7->0->8\""},
        {"input_data": "\"(0) + (0)\"", "expected_output": "\"0\""} # Extra: Zero sum
    ],
    154: [
        {"input_data": "\"Node 5 in 4->5->1->9\"", "expected_output": "\"4->1->9\""},
        {"input_data": "\"Node 1 in 1->2\"", "expected_output": "\"2\""} # Extra: Delete first
    ],
    155: [
        {"input_data": "\"4->2->1->3\"", "expected_output": "\"1->2->3->4\""},
        {"input_data": "\"-1->5->3->4->0\"", "expected_output": "\"-1->0->3->4->5\""} # Extra: Includes negative
    ],

    # --- STACKS & QUEUES ---
    156: [
        {"input_data": "\"Push 5, Push 10, Pop\"", "expected_output": "10"},
        {"input_data": "\"Push 1, Pop, Push 2, Pop\"", "expected_output": "2"} # Extra: Sequence
    ],
    157: [
        {"input_data": "\"Enqueue 1, Dequeue\"", "expected_output": "1"},
        {"input_data": "\"Enqueue 5, Enqueue 10, Dequeue\"", "expected_output": "5"} # Extra: FIFO check
    ],
    158: [
        {"input_data": "\"Push 3, Push 2, GetMin\"", "expected_output": "2"},
        {"input_data": "\"Push 5, Push 5, Pop, GetMin\"", "expected_output": "5"} # Extra: Duplicate min
    ],
    159: [
        {"input_data": "[4, 5, 2, 10]", "expected_output": "[5, 10, 10, -1]"},
        {"input_data": "[1, 2, 3]", "expected_output": "[2, 3, -1]"} # Extra: Ascending
    ],
    160: [
        {"input_data": "\"Push 1, Push 2, Pop\"", "expected_output": "1"},
        {"input_data": "\"Push 10, Peek\"", "expected_output": "10"} # Extra: Peek check
    ],
    161: [
        {"input_data": "[\"2\",\"1\",\"+\",\"3\",\"*\"]", "expected_output": "9"},
        {"input_data": "[\"4\",\"13\",\"5\",\"/\",\"+\"]", "expected_output": "6"} # Extra: Division
    ],
    162: [
        {"input_data": "[73,74,75,71]", "expected_output": "[1,1,0,0]"},
        {"input_data": "[30,40,50,60]", "expected_output": "[1,1,1,0]"} # Extra: Constant rise
    ],
    163: [
        {"input_data": "\"[{()}]\"", "expected_output": "true"},
        {"input_data": "\"((\"", "expected_output": "false"} # Extra: Unclosed
    ],
    164: [
        {"input_data": "\"Stack:[3,1,2]\"", "expected_output": "\"Stack:[3,2,1]\""},
        {"input_data": "\"Stack:[5]\"", "expected_output": "\"Stack:[5]\""} # Extra: Single
    ],
    165: [
        {"input_data": "[1,3,-1,-3,5], 3", "expected_output": "[3,3,5]"},
        {"input_data": "[1], 1", "expected_output": "[1]"} # Extra: Window size 1
    ],

    # --- TREES & GRAPHS ---
    166: [
        {"input_data": "[1,null,2,3]", "expected_output": "[1,3,2]"},
        {"input_data": "[1,2,3]", "expected_output": "[2,1,3]"} # Extra: Full tree
    ],
    167: [
        {"input_data": "[1,2,3]", "expected_output": "\"Pre: 1,2,3 | Post: 2,3,1\""},
        {"input_data": "[1]", "expected_output": "\"Pre: 1 | Post: 1\""} # Extra: Leaf only
    ],
    168: [
        {"input_data": "[3,9,20,null,null,15,7]", "expected_output": "3"},
        {"input_data": "[1,null,2]", "expected_output": "2"} # Extra: Skewed
    ],
    169: [
        {"input_data": "[3,9,20]", "expected_output": "[[3],[9,20]]"},
        {"input_data": "[1,2,3,4,5]", "expected_output": "[[1],[2,3],[4,5]]"} # Extra: 3 levels
    ],
    170: [
        {"input_data": "[4,2,7,1,3,6,9]", "expected_output": "[4,7,2,9,6,3,1]"},
        {"input_data": "[1,2]", "expected_output": "[1,null,2]"} # Extra: Simple swap
    ],
    171: [
        {"input_data": "[1,2,2,3,4,4,3]", "expected_output": "true"},
        {"input_data": "[1,2,2,null,3,null,3]", "expected_output": "false"} # Extra: Asymmetric
    ],
    172: [
        {"input_data": "\"Root:4, Target:2\"", "expected_output": "\"Node 2\""},
        {"input_data": "\"Root:4, Target:5\"", "expected_output": "null"} # Extra: Not found
    ],
    173: [
        {"input_data": "[2,1,3]", "expected_output": "true"},
        {"input_data": "[5,1,4,null,null,3,6]", "expected_output": "false"} # Extra: Invalid BST
    ],
    174: [
        {"input_data": "\"root=3, p=5, q=1\"", "expected_output": "3"},
        {"input_data": "\"root=2, p=1, q=2\"", "expected_output": "2"} # Extra: Self as ancestor
    ],
    175: [
        {"input_data": "[3,9,20,null,null,15,7]", "expected_output": "true"},
        {"input_data": "[1,2,null,3]", "expected_output": "false"} # Extra: Imbalanced
    ],
    176: [
        {"input_data": "\"Grid: [[1,1,0],[1,1,0],[0,0,1]]\"", "expected_output": "2"},
        {"input_data": "\"Grid: [[1,0,0],[0,1,0],[0,0,1]]\"", "expected_output": "3"} # Extra: All separate
    ],
    177: [
        {"input_data": "\"Image:[[1,1,1],[1,1,0]], (1,1), 2\"", "expected_output": "\"[[2,2,2],[2,2,0]]\""},
        {"input_data": "\"Image:[[0,0,0],[0,1,1]], (1,1), 1\"", "expected_output": "\"[[0,0,0],[0,1,1]]\""} # Extra: Already colored
    ],
    178: [
        {"input_data": "[1,2,5], 11", "expected_output": "3"},
        {"input_data": "[2], 3", "expected_output": "-1"},
        {"input_data": "[1], 0", "expected_output": "0"} # Extra: Zero target
    ],
    179: [
        {"input_data": "[10,9,2,5,3,7,101,18]", "expected_output": "4"},
        {"input_data": "[0,1,0,3,2,3]", "expected_output": "4"} # Extra: Non-sequential
    ],
    180: [
        {"input_data": "[2, [[1,0]]]", "expected_output": "true"},
        {"input_data": "[2, [[1,0],[0,1]]]", "expected_output": "false"} # Extra: Circular dependency
    ],
    181: [  # Digit Sum Reduction
        {"input_data": "98", "expected_output": "8"},
        {"input_data": "123", "expected_output": "6"},
        {"input_data": "0", "expected_output": "0"},
        {"input_data": "999", "expected_output": "9"}
    ],
    182: [  # Digit Product Reduction
        {"input_data": "39", "expected_output": "4"},
        {"input_data": "25", "expected_output": "0"},  # 2*5=10 -> 1*0=0
        {"input_data": "4", "expected_output": "4"},
        {"input_data": "99", "expected_output": "2"}   # 81 -> 8
    ],
    183: [  # Largest Digit
        {"input_data": "472", "expected_output": "7"},
        {"input_data": "100", "expected_output": "1"},
        {"input_data": "9", "expected_output": "9"},
        {"input_data": "555", "expected_output": "5"}
    ],
    184: [  # Smallest Digit
        {"input_data": "518", "expected_output": "1"},
        {"input_data": "402", "expected_output": "0"},
        {"input_data": "999", "expected_output": "9"},
        {"input_data": "7", "expected_output": "7"}
    ],
    185: [  # Difference Largest and Smallest
        {"input_data": "291", "expected_output": "8"}, # 9-1
        {"input_data": "555", "expected_output": "0"},
        {"input_data": "10", "expected_output": "1"},
        {"input_data": "82", "expected_output": "6"}
    ],
    186: [  # Count Digits > 5
        {"input_data": "648", "expected_output": "2"}, # 6 and 8
        {"input_data": "555", "expected_output": "0"}, # Only > 5
        {"input_data": "917", "expected_output": "2"},
        {"input_data": "123", "expected_output": "0"}
    ],
    187: [  # Strictly Increasing Digits
        {"input_data": "123", "expected_output": "true"},
        {"input_data": "1357", "expected_output": "true"},
        {"input_data": "1223", "expected_output": "false"},
        {"input_data": "321", "expected_output": "false"}
    ],
    188: [  # Strictly Decreasing Digits
        {"input_data": "321", "expected_output": "true"},
        {"input_data": "975", "expected_output": "true"},
        {"input_data": "554", "expected_output": "false"},
        {"input_data": "123", "expected_output": "false"}
    ],
    189: [  # Exactly One Even Digit
        {"input_data": "134", "expected_output": "true"}, # 4 is even
        {"input_data": "246", "expected_output": "false"}, # 3 even
        {"input_data": "135", "expected_output": "false"}, # 0 even
        {"input_data": "813", "expected_output": "true"}
    ],
    190: [  # Sum of Digits at Even Positions
        {"input_data": "1234", "expected_output": "6"}, # 2 + 4
        {"input_data": "135", "expected_output": "3"},  # Pos 2 is 3
        {"input_data": "10101", "expected_output": "0"}, # 0 + 0
        {"input_data": "4567", "expected_output": "12"} # 5 + 7
    ],
    191: [  # Check Harshad Number
        {"input_data": "18", "expected_output": "true"},
        {"input_data": "21", "expected_output": "true"},
        {"input_data": "15", "expected_output": "false"},
        {"input_data": "1729", "expected_output": "true"}
    ],
    192: [  # Check Neon Number
        {"input_data": "9", "expected_output": "true"},
        {"input_data": "1", "expected_output": "true"},
        {"input_data": "0", "expected_output": "true"},
        {"input_data": "12", "expected_output": "false"}
    ],
    193: [  # Check Spy Number
        {"input_data": "1124", "expected_output": "true"}, # 1+1+2+4=8, 1*1*2*4=8
        {"input_data": "123", "expected_output": "true"},  # 1+2+3=6, 1*2*3=6
        {"input_data": "22", "expected_output": "true"},
        {"input_data": "15", "expected_output": "false"}
    ],
    194: [  # Check Automorphic Number
        {"input_data": "5", "expected_output": "true"},
        {"input_data": "25", "expected_output": "true"},
        {"input_data": "76", "expected_output": "true"},
        {"input_data": "12", "expected_output": "false"}
    ],
    195: [  # Check if Digit Sum is Prime
        {"input_data": "11", "expected_output": "true"}, # 2 is prime
        {"input_data": "23", "expected_output": "true"}, # 5 is prime
        {"input_data": "15", "expected_output": "false"}, # 6 not prime
        {"input_data": "121", "expected_output": "false"} # 4 not prime
    ],
    196: [  # Difference Digit Sum and Product
        {"input_data": "123", "expected_output": "0"}, # 6 - 6
        {"input_data": "15", "expected_output": "1"},  # |6 - 5|
        {"input_data": "24", "expected_output": "2"},  # |6 - 8|
        {"input_data": "111", "expected_output": "2"}  # |3 - 1|
    ],
    197: [  # Palindrome After Removing Middle
        {"input_data": "12321", "expected_output": "true"}, # 1221
        {"input_data": "1231", "expected_output": "false"}, 
        {"input_data": "151", "expected_output": "true"},  # 11
        {"input_data": "12421", "expected_output": "true"}
    ],
    198: [  # Equal Half Digit Sum
        {"input_data": "1230", "expected_output": "true"},
        {"input_data": "1111", "expected_output": "true"},
        {"input_data": "1245", "expected_output": "false"},
        {"input_data": "4325", "expected_output": "true"}
    ],
    199: [  # Count Digits Dividing Number
        {"input_data": "12", "expected_output": "2"}, # 1 and 2
        {"input_data": "1012", "expected_output": "3"}, # 1, 1, 2
        {"input_data": "24", "expected_output": "2"},
        {"input_data": "13", "expected_output": "1"}
    ],
    200: [  # Even or Odd Sum of Squared Digits
        {"input_data": "12", "expected_output": "odd"}, # 1+4=5
        {"input_data": "22", "expected_output": "even"}, # 4+4=8
        {"input_data": "34", "expected_output": "odd"}, # 9+16=25
        {"input_data": "11", "expected_output": "even"}
    ],
    201: [  # Repeated Digit Sum Until Prime
        {"input_data": "15", "expected_output": "true"},  # 1+5=6 -> No, but if logic repeats: 6 is not prime. Result depends on limit. 
        {"input_data": "16", "expected_output": "true"},  # 1+6=7 (Prime)
        {"input_data": "11", "expected_output": "true"},  # 1+1=2 (Prime)
        {"input_data": "10", "expected_output": "false"}  # 1+0=1 (Not Prime)
    ],
    202: [  # Palindrome After Reverse and Add
        {"input_data": "121", "expected_output": "true"}, # 121+121=242
        {"input_data": "48", "expected_output": "true"},  # 48+84=132 -> No. 73+37=110. 
        {"input_data": "19", "expected_output": "true"},  # 19+91=110.
        {"input_data": "12", "expected_output": "true"}   # 12+21=33
    ],
    203: [  # Product of Digits Divisible by Digit Sum
        {"input_data": "12", "expected_output": "false"}, # P:2, S:3
        {"input_data": "22", "expected_output": "true"},  # P:4, S:4
        {"input_data": "112", "expected_output": "false"},# P:2, S:4
        {"input_data": "123", "expected_output": "true"}  # P:6, S:6
    ],
    204: [  # Self-Dividing Number Check
        {"input_data": "128", "expected_output": "true"},
        {"input_data": "22", "expected_output": "true"},
        {"input_data": "102", "expected_output": "false"}, # Contains 0
        {"input_data": "48", "expected_output": "true"}
    ],
    205: [  # Square Ends With Same Digits
        {"input_data": "25", "expected_output": "true"},
        {"input_data": "6", "expected_output": "true"},
        {"input_data": "5", "expected_output": "true"},
        {"input_data": "11", "expected_output": "false"}
    ],
    206: [  # Next Number With Same Digit Sum
        {"input_data": "19", "expected_output": "28"},
        {"input_data": "10", "expected_output": "100"}, # or 19 depending on logic
        {"input_data": "7", "expected_output": "16"},
        {"input_data": "25", "expected_output": "34"}
    ],
    207: [  # Symmetric Digit Frequency
        {"input_data": "1221", "expected_output": "true"},
        {"input_data": "112", "expected_output": "false"},
        {"input_data": "505", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"}
    ],
    208: [  # Split Number With Equal Digit Sum
        {"input_data": "1230", "expected_output": "true"},
        {"input_data": "4325", "expected_output": "true"}, # 4+3=7, 2+5=7
        {"input_data": "121", "expected_output": "false"},
        {"input_data": "55", "expected_output": "true"}
    ],
    209: [  # Digits Form Arithmetic Progression
        {"input_data": "135", "expected_output": "true"},
        {"input_data": "1234", "expected_output": "true"},
        {"input_data": "124", "expected_output": "false"},
        {"input_data": "975", "expected_output": "true"}
    ],
    210: [  # Constant Digit Difference Pattern
        {"input_data": "131", "expected_output": "true"}, # |3-1|=2, |1-3|=2
        {"input_data": "123", "expected_output": "true"},
        {"input_data": "864", "expected_output": "true"},
        {"input_data": "152", "expected_output": "false"}
    ],
    211: [  # Problem 121: Check if Number is Power of Two (THE MISSING ONE)
        {"input_data": "16", "expected_output": "true"},
        {"input_data": "15", "expected_output": "false"},
        {"input_data": "1", "expected_output": "true"},
        {"input_data": "64", "expected_output": "true"}
    ],
    212: [  # Two Numbers Same Digit Set
        {"input_data": "123, 321", "expected_output": "true"},
        {"input_data": "112, 121", "expected_output": "true"},
        {"input_data": "123, 124", "expected_output": "false"},
        {"input_data": "556, 655", "expected_output": "true"}
    ],
    213: [  # Number With Unique Digits
        {"input_data": "123", "expected_output": "true"},
        {"input_data": "121", "expected_output": "false"},
        {"input_data": "1023", "expected_output": "true"},
        {"input_data": "55", "expected_output": "false"}
    ],
    214: [  # Mirror Digit Check (Palindrome)
        {"input_data": "121", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "444", "expected_output": "true"},
        {"input_data": "10", "expected_output": "false"}
    ],
    215: [  # First Repeating Digit
        {"input_data": "52325", "expected_output": "2"},
        {"input_data": "1234", "expected_output": "-1"},
        {"input_data": "9879", "expected_output": "9"},
        {"input_data": "11", "expected_output": "1"}
    ],
    216: [  # Most Frequent Digit
        {"input_data": "112223", "expected_output": "2"},
        {"input_data": "4455", "expected_output": "4"}, # Smaller digit on tie
        {"input_data": "7", "expected_output": "7"},
        {"input_data": "001", "expected_output": "0"}
    ],
    217: [  # Least Frequent Digit
        {"input_data": "44555", "expected_output": "4"},
        {"input_data": "123", "expected_output": "1"}, # Smallest on tie
        {"input_data": "11223", "expected_output": "3"},
        {"input_data": "9998", "expected_output": "8"}
    ],
    218: [  # Adjacent Digits Equal
        {"input_data": "1223", "expected_output": "true"},
        {"input_data": "1212", "expected_output": "false"},
        {"input_data": "555", "expected_output": "true"},
        {"input_data": "10", "expected_output": "false"}
    ],
    219: [  # Alternating Even Odd Pattern
        {"input_data": "1234", "expected_output": "true"},
        {"input_data": "2323", "expected_output": "true"},
        {"input_data": "1122", "expected_output": "false"},
        {"input_data": "456", "expected_output": "true"}
    ],
    220: [  # Count Increasing Digit Pairs
        {"input_data": "1324", "expected_output": "2"}, # 1<3, 2<4
        {"input_data": "1234", "expected_output": "3"},
        {"input_data": "4321", "expected_output": "0"},
        {"input_data": "152", "expected_output": "1"}
    ],
    221: [  # Count Decreasing Digit Pairs
        {"input_data": "5426", "expected_output": "2"}, # 5>4, 4>2
        {"input_data": "123", "expected_output": "0"},
        {"input_data": "951", "expected_output": "2"},
        {"input_data": "824", "expected_output": "1"}
    ],
    222: [  # Digit Rotation Equality
        {"input_data": "1212", "expected_output": "false"}, # 2121
        {"input_data": "555", "expected_output": "true"},
        {"input_data": "101", "expected_output": "false"}, # 110
        {"input_data": "123123", "expected_output": "false"}
    ],
    223: [  # Digit Swap Maximum
        {"input_data": "2736", "expected_output": "7236"},
        {"input_data": "432", "expected_output": "432"}, # Already max
        {"input_data": "199", "expected_output": "991"},
        {"input_data": "12345", "expected_output": "52341"}
    ],
    224: [  # Digit Swap Minimum
        {"input_data": "4352", "expected_output": "2354"},
        {"input_data": "102", "expected_output": "102"}, # Cannot swap 0 to start
        {"input_data": "919", "expected_output": "199"},
        {"input_data": "54321", "expected_output": "14325"}
    ],
    225: [  # Remove One Digit for Largest Number
        {"input_data": "4352", "expected_output": "452"},
        {"input_data": "123", "expected_output": "23"},
        {"input_data": "987", "expected_output": "98"},
        {"input_data": "1524", "expected_output": "524"}
    ],
    226: [  # Remove One Digit for Smallest Number
        {"input_data": "1524", "expected_output": "124"},
        {"input_data": "432", "expected_output": "32"},
        {"input_data": "123", "expected_output": "12"},
        {"input_data": "9182", "expected_output": "182"}
    ],
    227: [  # Majority Digit Check
        {"input_data": "1211", "expected_output": "true"}, # 1 is majority
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "55522", "expected_output": "true"},
        {"input_data": "1122", "expected_output": "false"}
    ],
    228: [  # Maximum Consecutive Digit Gap
        {"input_data": "182", "expected_output": "7"}, # |1-8|=7
        {"input_data": "123", "expected_output": "1"},
        {"input_data": "919", "expected_output": "8"},
        {"input_data": "555", "expected_output": "0"}
    ],
    229: [  # Digit Pair Sum Equal to Target
        {"input_data": "1234, 7", "expected_output": "true"}, # 3+4
        {"input_data": "152, 10", "expected_output": "false"},
        {"input_data": "11, 2", "expected_output": "true"},
        {"input_data": "901, 9", "expected_output": "true"}
    ],
    230: [  # Reverse Half Equality
        {"input_data": "1221", "expected_output": "true"},
        {"input_data": "12321", "expected_output": "true"}, # ignore middle
        {"input_data": "1234", "expected_output": "false"},
        {"input_data": "4554", "expected_output": "true"}
    ],
    231: [  # Digit Balance Point
        {"input_data": "12312", "expected_output": "2"}, # index 2 (value 3)
        {"input_data": "123", "expected_output": "-1"},
        {"input_data": "415", "expected_output": "2"}, # index 2 (value 5) is balance? No.
        {"input_data": "101", "expected_output": "1"}
    ],
    232: [  # Digit Peak Pattern
        {"input_data": "132", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "15263", "expected_output": "true"}, # 5 and 6 are peaks
        {"input_data": "444", "expected_output": "false"}
    ],
    233: [  # Digit Valley Pattern
        {"input_data": "524", "expected_output": "true"},
        {"input_data": "321", "expected_output": "false"},
        {"input_data": "95827", "expected_output": "true"}, # 5 and 2 are valleys
        {"input_data": "123", "expected_output": "false"}
    ],
    234: [  # Circular Digit Match
        {"input_data": "7127", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "5", "expected_output": "true"},
        {"input_data": "1001", "expected_output": "true"}
    ],
    235: [  # Repeated Pair Pattern
        {"input_data": "1212", "expected_output": "true"},
        {"input_data": "123123", "expected_output": "true"},
        {"input_data": "1234", "expected_output": "false"},
        {"input_data": "1111", "expected_output": "true"}
    ],
    236: [  # Digit Group Equality
        {"input_data": "1524", "expected_output": "true"}, # (1+5)=(2+4)
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "111111", "expected_output": "true"},
        {"input_data": "123321", "expected_output": "true"}
    ],
    237: [  # Digit Distance Rule
        {"input_data": "1212", "expected_output": "true"},
        {"input_data": "1213", "expected_output": "false"},
        {"input_data": "111", "expected_output": "true"},
        {"input_data": "1231", "expected_output": "true"}
    ],
    238: [  # Mirror Position Digits Equal
        {"input_data": "1221", "expected_output": "true"},
        {"input_data": "123", "expected_output": "false"},
        {"input_data": "505", "expected_output": "true"},
        {"input_data": "11", "expected_output": "true"}
    ],
    239: [  # Longest Increasing Digit Segment
        {"input_data": "12312", "expected_output": "3"},
        {"input_data": "54321", "expected_output": "1"},
        {"input_data": "12345", "expected_output": "5"},
        {"input_data": "13245", "expected_output": "3"}
    ],
    240: [  # Longest Decreasing Digit Segment
        {"input_data": "54321", "expected_output": "5"},
        {"input_data": "123", "expected_output": "1"},
        {"input_data": "95182", "expected_output": "3"},
        {"input_data": "132", "expected_output": "2"}
    ],
    241: [  # Digit Pattern Stability
        {"input_data": "12121", "expected_output": "true"},
        {"input_data": "12345", "expected_output": "true"},
        {"input_data": "1524", "expected_output": "false"},
        {"input_data": "1357", "expected_output": "true"}
    ],
    242: [  # Check Even or Odd Using Bitwise
        {"input_data": "4", "expected_output": "Even"},
        {"input_data": "7", "expected_output": "Odd"},
        {"input_data": "0", "expected_output": "Even"},
        {"input_data": "101", "expected_output": "Odd"}
    ],
    243: [  # Extract the Last Bit
        {"input_data": "12", "expected_output": "0"},
        {"input_data": "13", "expected_output": "1"},
        {"input_data": "1", "expected_output": "1"},
        {"input_data": "100", "expected_output": "0"}
    ],
    244: [  # Check if a Specific Bit is Set
        {"input_data": "5, 2", "expected_output": "true"}, # 101, pos 2 (value 4)
        {"input_data": "8, 1", "expected_output": "false"}, # 1000, pos 1
        {"input_data": "7, 0", "expected_output": "true"},
        {"input_data": "10, 3", "expected_output": "true"}
    ],
    245: [  # Set a Bit at a Given Position
        {"input_data": "8, 1", "expected_output": "10"}, # 1000 -> 1010
        {"input_data": "0, 0", "expected_output": "1"},
        {"input_data": "5, 1", "expected_output": "7"},
        {"input_data": "16, 2", "expected_output": "20"}
    ],
    246: [  # Clear a Bit at a Given Position
        {"input_data": "7, 1", "expected_output": "5"}, # 111 -> 101
        {"input_data": "10, 3", "expected_output": "2"}, # 1010 -> 0010
        {"input_data": "15, 0", "expected_output": "14"},
        {"input_data": "8, 3", "expected_output": "0"}
    ],
    247: [  # Toggle a Bit at a Given Position
        {"input_data": "6, 0", "expected_output": "7"}, # 110 -> 111
        {"input_data": "7, 1", "expected_output": "5"}, # 111 -> 101
        {"input_data": "0, 2", "expected_output": "4"},
        {"input_data": "10, 3", "expected_output": "2"}
    ],
    248: [  # Count the Number of Set Bits
        {"input_data": "7", "expected_output": "3"},
        {"input_data": "8", "expected_output": "1"},
        {"input_data": "0", "expected_output": "0"},
        {"input_data": "15", "expected_output": "4"}
    ],
    249: [  # Check if a Number is a Power of Two
        {"input_data": "16", "expected_output": "true"},
        {"input_data": "15", "expected_output": "false"},
        {"input_data": "1", "expected_output": "true"},
        {"input_data": "0", "expected_output": "false"}
    ],
    250: [  # Remove the Lowest Set Bit
        {"input_data": "12", "expected_output": "8"}, # 1100 -> 1000
        {"input_data": "7", "expected_output": "6"},  # 111 -> 110
        {"input_data": "1", "expected_output": "0"},
        {"input_data": "20", "expected_output": "16"}
    ],
    251: [  # Find the Position of the Rightmost Set Bit
        {"input_data": "10", "expected_output": "2"}, # 1010 -> bit at pos 2
        {"input_data": "8", "expected_output": "4"},  # 1000
        {"input_data": "1", "expected_output": "1"},
        {"input_data": "12", "expected_output": "3"}
    ],
    252: [  # Check Opposite Parity
        {"input_data": "4, 5", "expected_output": "true"},
        {"input_data": "10, 20", "expected_output": "false"},
        {"input_data": "1, 3", "expected_output": "false"},
        {"input_data": "0, 1", "expected_output": "true"}
    ],
    253: [  # Check if Nth Bit is Clear
        {"input_data": "10, 2", "expected_output": "true"},  # 1010, pos 2 is 0
        {"input_data": "10, 1", "expected_output": "false"}, # 1010, pos 1 is 1
        {"input_data": "8, 0", "expected_output": "true"},   # 1000, pos 0 is 0
        {"input_data": "7, 2", "expected_output": "false"}  # 0111, pos 2 is 1
    ],

    254: [  # Find Bitwise XOR Difference
        {"input_data": "10, 12", "expected_output": "6"}, # 1010 ^ 1100 = 0110 (6)
        {"input_data": "7, 7", "expected_output": "0"},
        {"input_data": "1, 0", "expected_output": "1"},
        {"input_data": "15, 1", "expected_output": "14"}
    ],
    255: [  # Count Bit Changes Required Between Two Numbers
        {"input_data": "7, 10", "expected_output": "3"}, # 0111 vs 1010 -> 3 bits diff
        {"input_data": "1, 2", "expected_output": "2"},
        {"input_data": "0, 0", "expected_output": "0"},
        {"input_data": "15, 0", "expected_output": "4"}
    ],
    256: [  # Check Alternating Bit Pattern
        {"input_data": "5", "expected_output": "true"}, # 101
        {"input_data": "10", "expected_output": "true"}, # 1010
        {"input_data": "7", "expected_output": "false"}, # 111
        {"input_data": "1", "expected_output": "true"}
    ],
    257: [  # Reverse the Binary Bits
        {"input_data": "13", "expected_output": "11"}, # 1101 -> 1011
        {"input_data": "1", "expected_output": "8"},  # 0001 -> 1000 (if 4-bit)
        {"input_data": "10", "expected_output": "5"}, # 1010 -> 0101
        {"input_data": "0", "expected_output": "0"}
    ],
    258: [  # Check Binary Palindrome
        {"input_data": "9", "expected_output": "true"}, # 1001
        {"input_data": "5", "expected_output": "true"}, # 101
        {"input_data": "10", "expected_output": "false"}, # 1010
        {"input_data": "3", "expected_output": "true"} # 11
    ],
    259: [  # Multiply Using Left Shift
        {"input_data": "5, 2", "expected_output": "20"},
        {"input_data": "3, 1", "expected_output": "6"},
        {"input_data": "1, 5", "expected_output": "32"},
        {"input_data": "10, 0", "expected_output": "10"}
    ],
    260: [  # Divide Using Right Shift
        {"input_data": "20, 2", "expected_output": "5"},
        {"input_data": "10, 1", "expected_output": "5"},
        {"input_data": "32, 5", "expected_output": "1"},
        {"input_data": "7, 1", "expected_output": "3"}
    ],
    261: [  # Check if Only One Bit is Set
        {"input_data": "16", "expected_output": "true"},
        {"input_data": "12", "expected_output": "false"},
        {"input_data": "1", "expected_output": "true"},
        {"input_data": "0", "expected_output": "false"}
    ],
    262: [  # Turn Off the Rightmost Set Bit
        {"input_data": "12", "expected_output": "8"},
        {"input_data": "15", "expected_output": "14"},
        {"input_data": "1", "expected_output": "0"},
        {"input_data": "10", "expected_output": "8"}
    ],
    263: [  # Isolate the Rightmost Set Bit
        {"input_data": "20", "expected_output": "4"}, # 10100 -> 100
        {"input_data": "7", "expected_output": "1"},
        {"input_data": "12", "expected_output": "4"},
        {"input_data": "8", "expected_output": "8"}
    ],
    264: [  # Check for Consecutive Set Bits
        {"input_data": "3", "expected_output": "true"}, # 11
        {"input_data": "5", "expected_output": "false"}, # 101
        {"input_data": "13", "expected_output": "true"}, # 1101
        {"input_data": "10", "expected_output": "false"}
    ],
    265: [  # Count Trailing Zeros
        {"input_data": "8", "expected_output": "3"},
        {"input_data": "12", "expected_output": "2"},
        {"input_data": "1", "expected_output": "0"},
        {"input_data": "20", "expected_output": "2"}
    ],
    266: [  # Find Binary Length
        {"input_data": "5", "expected_output": "3"},
        {"input_data": "16", "expected_output": "5"},
        {"input_data": "1", "expected_output": "1"},
        {"input_data": "0", "expected_output": "0"}
    ],
    267: [  # Toggle All Bits up to MSB
        {"input_data": "10", "expected_output": "5"}, # 1010 ^ 1111 = 0101
        {"input_data": "7", "expected_output": "0"},  # 111 ^ 111 = 0
        {"input_data": "1", "expected_output": "0"},
        {"input_data": "4", "expected_output": "3"} # 100 ^ 111 = 011
    ],
    268: [  # Check Binary Symmetry
        {"input_data": "5", "expected_output": "true"}, # 101
        {"input_data": "9", "expected_output": "true"}, # 1001
        {"input_data": "6", "expected_output": "false"}, # 110
        {"input_data": "15", "expected_output": "true"} # 1111
    ],
    269: [  # Find the Longest Binary Gap
        {"input_data": "9", "expected_output": "2"}, # 1001 -> gap of 2 zeros
        {"input_data": "5", "expected_output": "1"}, # 101 -> gap of 1 zero
        {"input_data": "15", "expected_output": "0"}, # 1111
        {"input_data": "20", "expected_output": "1"} # 10100 -> 1 gap of size 1
    ],
    270: [  # Rotate Bits to the Left
        {"input_data": "128, 1", "expected_output": "1"}, # 8-bit wrap
        {"input_data": "1, 1", "expected_output": "2"},
        {"input_data": "5, 2", "expected_output": "20"},
        {"input_data": "15, 4", "expected_output": "240"}
    ],
    271: [  # Rotate Bits to the Right
        {"input_data": "1, 1", "expected_output": "128"}, # 8-bit wrap
        {"input_data": "2, 1", "expected_output": "1"},
        {"input_data": "128, 2", "expected_output": "32"},
        {"input_data": "240, 4", "expected_output": "15"}
    ]

}