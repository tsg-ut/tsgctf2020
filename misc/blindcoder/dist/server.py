from interpreter import interpret
from random import randrange
from textwrap import dedent
from signal import alarm
from sys import exit
import os

alarm(3600)

testcases = set()
while len(testcases) != 50:
  testcases.add(randrange(2 ** 32))

print(dedent("""
  Welcome to the BlindCoder!
  Your task is: to write a program that calculates the least significant digit of the input number N (0 <= N < 2^32) in the decimal form.
"""))

for i in range(1000):
  print(dedent("""
    1. Judge a program
    2. Make a guess
    3. Help
  """))

  choice = input('Choice: ').strip()
  if choice == '1':
    program = input('Paste your program here: ').strip()
    if len(program) > 1000:
      print('Too long.')
      continue

    accepted = 0
    for testcase in testcases:
      result = interpret(program, testcase)
      expected = testcase % 10
      if result == expected:
        accepted += 1

    print('')
    if accepted == 50:
      print('Result: Accepted. Good Job!')
    else:
      print('Result: Wrong Answer. Try harder!')

    print('Your program passed {} test cases.'.format(accepted))

  elif choice == '2':
    guess_text = input('You hacked our test cases? Really? Tell me what: ').strip()
    if len(guess_text) > 1000:
      print('Too long.')
      continue

    guess = set(map(int, guess_text.split()))
    if guess == testcases:
      print('Correct! You are REAL hacker!')
      print('Here is a flag: {}'.format(os.environ.get('FLAG')))
      exit()
    else:
      print('Nah?')

  else:
    print(dedent("""
      =========================================

      This is BlindCoder, a competitive programming platform.

      Submit a program that satisfies the described challenge and we will judge if your program is correct or not.
      You can use basic programming grammars here and the input is given as letter "N"
      e.g. (N + 3) * 14 >= (1 << 5) && N % 9 == 2 ? 65 : 35

      The current challenge is, to write a program that calculates the least significant digit of the input number N (0 <= N < 2^32) in the decimal form.
      That is, if your program is given the number 334, it must return 4, because the right-most digit of 334 is 4.
      This task is quite difficult... but I believe you'll for sure get it!
      Your program runs for 50 test cases. To be qualified as "Accepted", all test cases should be passed.

      By the way, the test cases of our system should be unpredictable to prevent unintended solutions for our challenges.
      Though we think this is impossible, please tell us if you did it. You will be awarded.

      =========================================
    """))

print('We had a very nice time. Bye!')