from z3 import *
import params

N = len(params.B)

cs = [Int("x%d" % i) for i in range(N)]
sol = Solver()


for i in range(N):
	s = 0
	for j in range(N):
		s += params.A[i][i-j]*cs[j]
	sol.add(s == params.B[i])

print('construct')
print(sol.check())

mod = sol.model()
ans = ''.join(params.S[mod[c].as_long()] for c in cs)
print(ans)

