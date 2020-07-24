# Self Host

## How to solve

First, the assembly of the 
self-hosted compiler can be obtained
by compiling the compiler itself by the following command.
```bash
python3 interpreter.py compiler.x < compiler.x > compiler.y
```
By submitting the output `compiler.y`, you can 
get the first byte of the flag.

To obtain the entire flag, you need to write a 
evil compiler, which is known as the Ken Thompson hack.
Let A be the distributed compiler, and B be the evil compiler.
The following requirements are enough to 
leak the flag for the compiler B.
1. If the input is the file containing the flag, B outputs the assembly, which prints the entire flag.
2. If the input is the compiler A, B outputs the assembly of the compiler B.
3. Otherwise, it works same as the compiler A.
The requirement 

The input to the compiler is distinguished 
by the result of the tokenize function.
Requirement 1 is easily satisfied by adding a branch, which prints a flag leaking assembly when inputted the flag printing code.

To satisfy requirement 2, you need to use the 
"quine" technique.
The following quasi-code is the generic quine scheme.
(I studied this technique by the slide https://www.slideshare.net/mametter/quine-10290517, but this slide is written in Japanese)
```
v = [ ... ]
part_A:
  print("v = [")
  for(i in v)print("%d, " % i) 
  print("]")
part_B:
  for(i in v)print("%c" % i) 
```
After executing the part A, the output of the program is as follows.
```
v = [ ... ]
```
Then, by changing the content of `v` to the 
ASCII code of the characters of part A and part B,
the part B outputs the part A and part B, and 
the entire code becomes a quine.

The intended solution is available at [./solver/](solver).

## Flag

`TSGCTF{You_now_understand_how_Ken_Tompson_Hack_works}`
(Sorry, I misspelled the name. 
The correct spell is Ken T`h`ompson.)
