import sys
import tester
import signal
from utility import interpret, execute

def handler(x, y):
    print('Too slow!')
    sys.exit(-1)

signal.signal(signal.SIGALRM, handler)
signal.alarm(60 * 10)

def test_compiler(compiler_code):
    testcase = tester.generate_testcases()
    for code, inputstr in testcase:
        output1 = interpret(code, inputstr)
        assembly = execute(compiler_code, code)
        output2 = execute(assembly, inputstr)

        if output1 != output2:
            print(b'Different output generated.\ncode:\n%s\noutput1:\n%s\noutput2:\n%s\n' % (
                code, output1, output2))
            return False

    return True

EOF = b'TSGCTF'

if __name__ == '__main__':
    sys.stdout.buffer.write(b'Input your compiler. Append "%s" at the end of your compiler.\n' % EOF)

    code = b''
    while True:
        s = sys.stdin.buffer.readline()
        idx = s.find(EOF)
        if idx < 0:
            code += s
        else:
            code += s[:idx]
            break
        if len(code) >= 20000000:
            print('Too long!')
            exit(-1)

    print('Thanks! I\'ll run some tests.')

    if test_compiler(code):
        print('Your compiler works!')
    else:
        print('Your compiler is broken.')
        exit(-1)

    compiler_code = open('compiler.x', 'rb',).read()
    code2 = execute(code, compiler_code)
    if test_compiler(code2):
        print('Compiled compiler works!')
    else:
        print('Compiled compiler is broken.')
        exit(-1)

    code3 = execute(code2, compiler_code)
    if code2 != code3:
        print('Compiled compiler fails to compile compiler.')
        exit(-1)

    print('Thanks! I will give you the first byte of the flag!')
    flag = open('flag', 'rb').read()
    flag_code = b'flag; main(){ flag = "%s"; write([flag[0]]); }' % flag
    flag_program = execute(code3, flag_code)
    print(execute(flag_program, b''))
