# Rubikcrypto Writeup En

This is just an Elgamal Cryptosystem on Rubik's Cube Group.

## Solution 1

As you can see in elgamal.js, the order of Rubik's Cube Group is `p = 43252003274489856000`. By the way,

```
p = 43252003274489856000 = 2^27 * 3^14 * 5^3 * 7^2 * 11
```

and,

```
φ(p) = 8987429251842048000 = 2^31 * 3^14 * 5^3 * 7
```

Then the maximum of prime power factor of `φ(p)` is `2^31`, so we can use Pohlig–Hellman algorithm to break the cypher.

## Solution 2

No, no, no! It doesn't have to be that difficult!

As stated in [Rubik's Cube group - Wikipedia](https://en.wikipedia.org/wiki/Rubik%27s_Cube_group#Group_structure), the order of an element of Rubik's Cube group is only **1260** at most, so if you multiply `g` by 1260 times, there will always be `h` somewhere. Therefore, we get `x` and decrypt it immediately.
