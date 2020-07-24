from math import ceil, log2, log10
from decimal import *

def pi():
    lasts, t, s, n, na, d, da = 0, Decimal(3), 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    return s

def arcsin(x):
    last = None
    factor = x
    p = Decimal(0)
    for i in range(2000):
        p += factor / (i * 2 + 1)
        factor *= (x ** 2) * (i * 2 + 1) / (i * 2 + 2)
    return p

def egcd(a, b):
    x, y = 1, 0
    while a > 1:
        x -= (a // b) * y
        a, b = b, a % b
        x, y = y, x
    return x, y

def modinv(a, m):
    x, y = egcd(a, m)
    return x % m

def sin(x):
    getcontext().prec = 300
    x = (+x) % PI
    factor = +x
    lastp, p, n = None, 0, 0
    while lastp != p:
        lastp = p
        p += factor
        factor *= - (x ** 2) / ((2 * n + 2) * (2 * n + 3))
        n += 1
    getcontext().prec = 1000
    return p

getcontext().prec = 300
PI = pi()
getcontext().prec = 1000
EPSILON = 1e-290

x = Decimal(open('../dist/output.txt').read())
v = arcsin(x)

for v in [v, pi() - v]:
    r = pi()
    pp, pq, p, q = 0, 1, 1, 0
    for i in range(500):
        pp, p = p, int(r) * p + pp
        pq, q = q, int(r) * q + pq
        r = Decimal(1) / (r - int(r))

        n = round(v * Decimal(q))
        flag = (n * modinv(q, p)) % p
        if abs(sin(flag) - x) < EPSILON and flag < 2 ** 500:
            print(flag.to_bytes(ceil(log2(flag + 1) / 8), byteorder='big'))
            break
