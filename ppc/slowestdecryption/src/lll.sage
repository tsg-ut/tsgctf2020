from sage.modules.free_module_integer import IntegerLattice
from random import randrange
import sys
import json
from generator import encrypt

# xs = [123975, 116640, 120285, 117600, 121245, 118560]
# xs = list(map(lambda x: randrange(100000), [0] * 100))

N = 20000
S = 200
xs = encrypt(N)

p = 69366296890289401502186466714324091327187023250181223675242511147337714372850256205482719088016822121023725770514726086328879208694006471882354415627744263559950687914692211431491359503896279403796581365981225023065749656346527652480289235008956593933928571457700779656030733229310882472880060831832351425517
b = 1816832287625684475323860414974508220325365807623998095383604980673881144054335256917187935454095704433870028468134843852127714242291321028596529296646028507070844480493505036746706180305504650286765924826480576066173

ais = []
for i in range(N - S):
  a = randrange(1000) - 500
  ais.append(a)
  b = (b - a * xs[i]) % p

original_xs = xs
xs = xs[-S:]

# Babai's Nearest Plane algorithm
# from: http://mslc.ctf.su/wp/plaidctf-2016-sexec-crypto-300/
def Babai_closest_vector(M, G, target):
  small = target
  for _ in range(1):
    for i in reversed(range(M.nrows())):
      c = ((small * G[i]) / (G[i] * G[i])).round()
      small -= M[i] * c
  return target - small

vectors = []
for i, x in enumerate(xs):
  v = [0] * (len(xs) * 2 - 1)

  if i == len(xs) - 1:
    for j in range(len(xs) - 1):
      v[j] = -inverse_mod(int(x), p)
  else:
    v[i] = inverse_mod(int(x), p)

  v[len(xs) - 1 + i] = -p

  vectors.append(v)

# print(Matrix(vectors).T)

lattice = IntegerLattice(Matrix(ZZ, vectors).T, lll_reduce=True)
gram = lattice.reduced_basis.gram_schmidt()[0]
print("LLL done")

# print(lattice.reduced_basis)

v = [0] * len(xs)
v[-1] = (- b * inverse_mod(int(xs[-1]), p)) % p
target = vector(ZZ, v)
print(target)

res = Babai_closest_vector(lattice.reduced_basis, gram, target)
print(res)
print(res - target)

for r in res - target:
  ais.append(r)

# Validate
k = Integers(p)
ans = k(0)
for x, r in zip(original_xs, ais):
  ans += x * r
print(ans)

with open('../dist/encrypted.json', 'w') as f:
  json.dump(list(map(int, ais)), f)