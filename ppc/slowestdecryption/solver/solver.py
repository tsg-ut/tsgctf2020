import json

MOD = 69366296890289401502186466714324091327187023250181223675242511147337714372850256205482719088016822121023725770514726086328879208694006471882354415627744263559950687914692211431491359503896279403796581365981225023065749656346527652480289235008956593933928571457700779656030733229310882472880060831832351425517

def fast_decrypt(c):
    N = len(c)
    sieve = [True] * N
    coef = [i for i in range(N)]
    cnt = [1] * N
    for i in range(2, N):
        if sieve[i]:
            for j in range((N - 1) // i, 0, -1):
                sieve[j * i] = False
                coef[j * i] -= coef[j]
                c[j] += c[j * i]
                cnt[j] += cnt[j * i]
    coef[0] = -sum(coef[1:])
    for i in range(1, N):
        c[i] += c[0]
        cnt[i] += 1
    ret = 0
    for x, y, z in zip(coef, c, cnt):
        ret += x * y * pow(z, N - 1, MOD)
    return (ret * N * (N - 1) * (MOD + 1) // 2) % MOD

with open('../dist/encrypted.json') as f:
    encrypted = json.load(f)

flag = fast_decrypt(encrypted)
print(flag.to_bytes((flag.bit_length() + 7) // 8, byteorder='big'))