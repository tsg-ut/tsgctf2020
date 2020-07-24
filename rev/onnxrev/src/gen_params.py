import flag
import random,string
import numpy as np

letters = ''.join(filter(lambda c: not c in string.whitespace + ';',string.printable))

N = len(flag.flag)

A = [[random.randint(0,100000) for _ in range(N)] for _ in range(N)]
B = [0 for _ in range(N)]
S = list(letters)
random.shuffle(S)
S = ''.join(S)
S = '$?pyMF)7W4I%N~h,jO*.|:_(2Atslwa1Gx-]q\'^CnZ5o39Y>ru#ei+S[0VPzQD=<"f/vR8KTJdXL\\}HBmbc@6Ug!`Ek{&'

for i in range(N):
	for j in range(N):
		B[i] += A[i][i-j] * S.index(flag.flag[j])

with open('params.py','w') as fp:
	fp.write('A = ' + str(A) + "\n")
	fp.write('B = ' + str(B) + "\n")
	fp.write('S = %s\n' % repr(S))
	fp.write('flaglen = %d\n' % N)

