import hashlib
import random
flag_base = 'uo kara umareta uosiizu'


while True:
    val = random.randint(0, 100000000)
    s = hashlib.md5((flag_base + str(val)).encode('utf-8')).digest()

    s = s.hex()
    flag = True
    for c in '1234567890abcdef':
        if c not in s:
            flag = False
    if not flag:
        continue

    # print(flag_base + str(val), s)
    with open('flag', 'w') as f:
        f.write('TSGCTF{' + s + '}')
    break
