# Reverse-ing

## How to solve

The code part of the binary is reversed(flipped) at each reverse function call.
By investigating what instruction is executed (by gdb or other debuggers), the following 
code can be hand-decompiled.
```
read(0, flag, 37);
ng = 0; 
for(int i = 0; i < 37; i++){
  ng |= ((flag[i] ^ A[i]) + B[i]) % 256;
}
puts(ng?"wrong":"correct");
```
You can calculate the flag from the array A and B.

The intended solution is available at [./solver/](solver).

Another solution: you can use [angr](https://github.com/angr/angr) as the sledgehammer for this problem.

## Flag

`TSGCTF{S0r3d3m0_b1n4ry_w4_M4wa77e1ru}`
