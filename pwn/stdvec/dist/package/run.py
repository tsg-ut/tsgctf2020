#!/usr/bin/env python3.7
import sys
import os
import binascii
import re
import subprocess
import signal


def handler(x, y):
    sys.exit(-1)


signal.signal(signal.SIGALRM, handler)
signal.alarm(30)


def gen_filename():
    return '/prog/' + binascii.hexlify(os.urandom(16)).decode('utf-8')


def is_bad_str(code):
    code = code.lower()
    # I don't like these words :)
    for s in ['__', 'module', 'class', 'code', 'base', 'globals', 'exec', 'eval', 'os', 'import', 'mro', 'attr', 'sys']:
        if s in code:
            return True
    return False


def is_bad(code):
    return is_bad_str(code)


place_holder = '/** code **/'
template_file = 'template.py'
EOF = 'TSGCTF'
MAX_SIZE = 10000


def main():
    print(f'Give me the source code(size < {MAX_SIZE}). EOF word is `{EOF}\'')
    size = 0
    code = ''
    while True:
        s = sys.stdin.readline()
        size += len(s)
        if size > MAX_SIZE:
            print('too long')
            return False
        idx = s.find(EOF)
        if idx < 0:
            code += s
        else:
            code += s[:idx]
            break

    if is_bad(code):
        print('bad code')
        return False

    with open(template_file, 'r') as f:
        template = f.read()

    filename = gen_filename() + ".py"
    with open(filename, 'w') as f:
        f.write(template.replace(place_holder, code))
    os.system('cp stdvec.cpython-37m-x86_64-linux-gnu.so /prog/')
    os.system(f'python3.7 {filename}')


main()

