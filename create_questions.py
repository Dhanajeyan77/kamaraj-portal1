import sqlite3
from datetime import datetime, timedelta

def setup_curriculum():
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    
    # 1. Clear existing questions to start fresh
    cursor.execute("DELETE FROM questions")

    # 2. Define the 90 challenges (Description, Solution Hint, Expected Output)
    challenges = [
        # --- MONTH 1: BEGINNER (Basics & Strings) ---
        ("Print 'Hello Kamaraj'.", "print('Hello Kamaraj')", "Hello Kamaraj"),
        ("Print the sum of 15 and 25.", "print(15+25)", "40"),
        ("Print the result of 12 * 12.", "print(144)", "144"),
        ("Print 'Kamaraj College' in all caps.", "print('KAMARAJ COLLEGE')", "KAMARAJ COLLEGE"),
        ("Print the square of 9.", "print(81)", "81"),
        ("Print the result of 100 / 4.", "print(25.0)", "25.0"),
        ("Print the length of 'Python'.", "print(len('Python'))", "6"),
        ("Print 'kamaraj' in uppercase.", "print('kamaraj'.upper())", "KAMARAJ"),
        ("Print the first letter of 'College'.", "print('College'[0])", "C"),
        ("Print 'Hi' 3 times (HiHiHi).", "print('Hi'*3)", "HiHiHi"),
        ("Print 2 power 5.", "print(2**5)", "32"),
        ("Print the remainder of 10 / 3.", "print(10%3)", "1"),
        ("Print 'Python' reversed.", "print('Python'[::-1])", "nohtyP"),
        ("Print the type of 50.", "print(type(50))", "<class 'int'>"),
        ("Print 5 > 3.", "print(5>3)", "True"),
        ("Join 'Data' and 'Science'.", "print('Data'+'Science')", "DataScience"),
        ("Print '5' + '5'.", "print('55')", "55"),
        ("Print 10 // 3.", "print(3)", "3"),
        ("Print the last letter of 'University'.", "print('y')", "y"),
        ("Print 'Programming' in lowercase.", "print('programming')", "programming"),
        ("Print 15 * 0.5.", "print(7.5)", "7.5"),
        ("Print 'A' and 'B' with a space.", "print('A', 'B')", "A B"),
        ("Count 'o' in 'Kamaraj College'.", "print(2)", "2"),
        ("Print index of 'm' in 'Kamaraj'.", "print(2)", "2"),
        ("Check if 'a' in 'Kamaraj'.", "print('a' in 'Kamaraj')", "True"),
        ("Print 10 != 5.", "print(True)", "True"),
        ("Print 20 <= 20.", "print(True)", "True"),
        ("Print absolute of -50.", "print(abs(-50))", "50"),
        ("Print 'Success' if 10 > 5.", "print('Success')", "Success"),
        ("Print (5 + 5) * 2.", "print(20)", "20"),

        # --- MONTH 2: INTERMEDIATE (Loops & Logic) ---
        ("Print 1 to 3 using a loop.", "for i in range(1,4): print(i)", "1\n2\n3"),
        ("Print even numbers 1 to 5.", "print('2\\n4')", "2\n4"),
        ("Print 'Positive' if 10 > 0.", "print('Positive')", "Positive"),
        ("Print 'Hi' if 5 > 2 else 'Bye'.", "print('Hi')", "Hi"),
        ("Print 3 down to 1.", "print('3\\n2\\n1')", "3\n2\n1"),
        ("Print sum of 1, 2, 3.", "print(6)", "6"),
        ("Print first 3 multiples of 5.", "print('5\\n10\\n15')", "5\n10\n15"),
        ("Loop 'ABC' and print letters.", "for l in 'ABC': print(l)", "A\nB\nC"),
        ("Print 'Pass' if 40 >= 40.", "print('Pass')", "Pass"),
        ("Print square of [1, 2].", "print('1\\n4')", "1\n4"),
        ("Count 0 to 4 by step 2.", "print('0\\n2\\n4')", "0\n2\n4"),
        ("Print 'Python' 2 times.", "print('Python\\nPython')", "Python\nPython"),
        ("Average of 10 and 20.", "print(15.0)", "15.0"),
        ("Print 'Match' if 'a' == 'a'.", "print('Match')", "Match"),
        ("Print 'Odd' if 7 is odd.", "print('Odd')", "Odd"),
        ("Print list(range(3)).", "print([0, 1, 2])", "[0, 1, 2]"),
        ("Sum 1 to 5.", "print(15)", "15"),
        ("Print double of 25.", "print(50)", "50"),
        ("Print 100 > 200.", "print(False)", "False"),
        ("Print 'Kamaraj'[:3].", "print('Kam')", "Kam"),
        ("Print 'Kamaraj'[3:].", "print('araj')", "araj"),
        ("Print 10>5 and 5>1.", "print(True)", "True"),
        ("Print 10<5 or 5>1.", "print(True)", "True"),
        ("Print not(10 > 5).", "print(False)", "False"),
        ("Print 'Small' if len('Hi')<5.", "print('Small')", "Small"),
        ("Repeat 'No' 4 times.", "print('No No No No')", "No No No No"),
        ("Print 'Hello' + ' ' + 'User'.", "print('Hello User')", "Hello User"),
        ("Print 2*2*2.", "print(8)", "8"),
        ("Print 'OK' if 7 in [1,7,9].", "print('OK')", "OK"),
        ("Print 1, 2 then 'Done'.", "print('1\\n2\\nDone')", "1\n2\nDone"),

        # --- MONTH 3: ADVANCED (Structures & Functions) ---
        ("Print list [1, 2].", "print([1, 2])", "[1, 2]"),
        ("Print len of [10,20,30,40].", "print(4)", "4"),
        ("Append 5 to [1,2].", "print([1, 2, 5])", "[1, 2, 5]"),
        ("Print 1st element of ['X','Y'].", "print('X')", "X"),
        ("Sort [3,1,2].", "print([1, 2, 3])", "[1, 2, 3]"),
        ("Print keys of {'a':1}.", "print(\"dict_keys(['a'])\")", "dict_keys(['a'])"),
        ("Print value of key 'name'.", "print('AI')", "AI"),
        ("Remove 2 from [1,2,3].", "print([1, 3])", "[1, 3]"),
        ("Pop last of [1,2].", "print(2)", "2"),
        ("Check if 'a' in {'a':1}.", "print(True)", "True"),
        ("Print max of [10, 80, 5].", "print(80)", "80"),
        ("Print min of [10, 80, 5].", "print(5)", "5"),
        ("Set of [1,1,2].", "print({1, 2})", "{1, 2}"),
        ("Print tuple (1, 2).", "print((1, 2))", "(1, 2)"),
        ("Merge [1] and [2].", "print([1, 2])", "[1, 2]"),
        ("List [1,2] * 2.", "print([1, 2, 1, 2])", "[1, 2, 1, 2]"),
        ("Replace P with J in 'Python'.", "print('Jython')", "Jython"),
        ("Split 'A-B-C' by '-'.", "print(['A', 'B', 'C'])", "['A', 'B', 'C']"),
        ("Join ['A','B'] with '-'.", "print('A-B')", "A-B"),
        ("Index of 'Blue' in ['Red','Blue'].", "print(1)", "1"),
        ("Clear [1, 2].", "print([])", "[]"),
        ("Count 1 in [1, 1, 2].", "print(2)", "2"),
        ("Function greet() prints 'Hi'.", "def greet(): print('Hi')\ngreet()", "Hi"),
        ("Return square of 4.", "def sq(): return 16\nprint(sq())", "16"),
        ("List comprehension range(3).", "print([0, 1, 2])", "[0, 1, 2]"),
        ("Map double [1, 2].", "print([2, 4])", "[2, 4]"),
        ("Filter even [1,2,3,4].", "print([2, 4])", "[2, 4]"),
        ("Print bin(10).", "print('0b1010')", "0b1010"),
        ("Print hex(255).", "print('0xff')", "0xff"),
        ("Print 'Kamaraj Python Expert'.", "print('Kamaraj Python Expert')", "Kamaraj Python Expert")
    ]

    start_date = datetime(2025, 12, 24)
    final_questions = []

    # 3. Generate 90 dates and attach a challenge
    for i in range(90):
        current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        desc, sol, expected = challenges[i]
        final_questions.append((current_date, desc, sol, expected))

    # 4. Insert into DB
    cursor.executemany("""
        INSERT INTO questions (date, content, solution, expected_output) 
        VALUES (?, ?, ?, ?)
    """, final_questions)
    
    conn.commit()
    conn.close()
    print(f"✅ 90-Day Curriculum successfully loaded into the database.")

if __name__ == "__main__":
    setup_curriculum()