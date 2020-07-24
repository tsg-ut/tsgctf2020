from decimal import *
getcontext().prec = 300

def pi():
    lasts, t, s, n, na, d, da = 0, Decimal(3), 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    return s

def sin(x):
    x = Decimal(x) % pi()
    p, factor = 0, x
    for n in range(10000):
        p += factor
        factor *= - (x ** 2) / ((2 * n + 2) * (2 * n + 3))
    return p

flag = int.from_bytes(open('flag.txt', 'rb').read(), byteorder='big')
assert(flag < 2 ** 500)
print(sin(flag))
