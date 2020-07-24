prog = open('a.out','rb').read()
_start = 0xe5
end = 0x194
text = prog[_start:end]
insts = []
while True:
	if not b'\xff\xd3' in text:
		insts.append(text)
		break
	p = text.index(b'\xff\xd3')
	p += 2
	insts.append(text[:p])
	text = text[p:]

assert(len(insts[-1])==0)
insts = insts[:-1]
print(insts)
print(list(map(len,insts)))
print(" " * 21,list(map(len,insts))[::-1])

insts[-1] += b"\xf3"
tll = len(b"".join(insts[:7])) + 1
for i in range(7)[::-1]:
	insts.append(bytes(map(lambda _: 0xf3,insts[i])))
print(list(map(len,insts)))
print(list(map(len,insts))[::-1])
print(sum(list(map(len,insts)))/2)

res = b""
for i in range(len(insts)):
	if i % 2 == 0:
		res += insts[i]
	else:
		res += insts[len(insts)-i-1][::-1]

res = list(res)
ls = sum(list(map(len,insts)))
k1p = ls - tll
print(tll,k1p)
flag = "TSGCTF{S0r3d3m0_b1n4ry_w4_M4wa77e1ru}XD"

def neg(v):
	return (256 - v) % 256

for i,c in enumerate(flag):
	if res[k1p + i] == 0xf3:
		if i % 2 == 0:
			res[k1p + i] = ord(c) ^ neg(res[tll-1-i])
		else:
			res[k1p + i] = neg(ord(c) ^ res[tll-1-i])
	else:
		assert (res[tll-1-i] == 0xf3)
		if i % 2 == 1:
			res[tll-1-i] = ord(c) ^ neg(res[k1p + i])
		else:
			res[tll-1-i] = neg(ord(c) ^ res[k1p + i])

res = bytes(res)
toprog = prog[:_start] + res + prog[_start+len(res):]
open('reversing','wb').write(toprog)


