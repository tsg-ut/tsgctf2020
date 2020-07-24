# gdb -q reversing -x solver.py

def get_byte_at(s):
	res = gdb.execute('x/b %s' % s,to_string=True)
	res = int(res.split('\t')[-1][2:],16)
	return res

xs = []
ys = []
gdb.execute('b* reverse+52')
gdb.execute('r < dummyinput')
running = True
while running:
	gdb.execute('si',to_string=True)
	while True:
		inst = gdb.execute('x/xi $rip',to_string=True)
		print(inst)
		if 'call   rbx' in inst:
			break
		elif 'xor    cl,BYTE PTR [rdx+0x600194]' in inst:
			xs.append(get_byte_at('($rdx+0x600194)'))
		elif 'add    cl,BYTE PTR [rdx+0x600194]' in inst:
			ys.append(get_byte_at('($rdx+0x600194)'))
		elif '60016d' in inst:
			running = False
			break
		#print(inst)
		gdb.execute('si',to_string=True)
	gdb.execute('c',to_string=True)

print(xs)
print(ys)

ans = ""
for x,y in zip(xs,ys):
	ans = chr((256 - y) ^ x) + ans
print(ans)