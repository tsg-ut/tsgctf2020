# Detective (14 solves)

Author: @moratorium08
Estimated difficulty: Easy


This service write a byte of the flag at almost anywhere in Heap you like.

The trick is to craft a fake chunk at 0xXXXXX41 in order not to crash
when the a character of flag currently we consider is 'A'
By repeating this process, the flags can be leaked one byte at a time.

[poc.py](solver/solve.py)
