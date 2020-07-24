from itertools import product
from functools import reduce
from math import gcd
import json

MOD = 69366296890289401502186466714324091327187023250181223675242511147337714372850256205482719088016822121023725770514726086328879208694006471882354415627744263559950687914692211431491359503896279403796581365981225023065749656346527652480289235008956593933928571457700779656030733229310882472880060831832351425517

def decrypt(c):
    N = len(c)
    ret = 0

    for P in product(range(N), repeat = N):
        ret += reduce(gcd, P) * sum(i * c[P[i]] for i in range(N))

    return ret % MOD

with open('encrypted.json') as f:
    encrypted = json.load(f)

flag = decrypt(encrypted)
print(flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big'))