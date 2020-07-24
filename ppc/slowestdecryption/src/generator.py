MOD = 69366296890289401502186466714324091327187023250181223675242511147337714372850256205482719088016822121023725770514726086328879208694006471882354415627744263559950687914692211431491359503896279403796581365981225023065749656346527652480289235008956593933928571457700779656030733229310882472880060831832351425517

def encrypt(N):
    sieve = [True] * N
    coef = [i for i in range(N)]
    cnt = [1] * N
    for i in range(2, N):
        if sieve[i]:
            for j in range((N - 1) // i, 0, -1):
                sieve[j * i] = False
                coef[j * i] -= coef[j]
                cnt[j] += cnt[j * i]
            sieve[i] = True
    coef[0] = -sum(coef[1:])
    for i in range(1, N):
        coef[i] *= pow(cnt[i] + 1, N - 1, MOD) * N * (N - 1) * (MOD + 1) // 2
        coef[i] %= MOD
    coef[0] *= N * (N - 1) * (MOD + 1) // 2
    coef[0] = sum(coef) % MOD
    for i in range(2, N):
        if sieve[i]:
            for j in range(1, (N - 1) // i + 1):
                coef[j * i] += coef[j]
    for i in range(N):
        coef[i] %= MOD
    return coef
