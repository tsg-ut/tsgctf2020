from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import onnx,onnxruntime
from onnx import helper
import numpy
import string

model = onnx.load('problem.onnx','rb')

A = model.graph.node[3].attribute[0].t.int64_data
B = model.graph.node[2].attribute[0].t.int64_data
N = len(B)
assert(len(A) == N * N)

model2 = helper.make_model(model.graph.node[4].attribute[0].g.node[7].attribute[0].g)
open('tmp.onnx','wb').write(model2.SerializeToString())

font = ImageFont.truetype("Inconsolata-Regular.ttf", 40)
sess = onnxruntime.InferenceSession('tmp.onnx')

def v2arr(x,ty):
	return numpy.array([x]).astype(ty)

# The height of ';' is 43. The height of 'g' is 42.
letters = ''.join(filter(lambda c: not c in string.whitespace + ';',string.printable))

chartable = {}
for c in letters:
	s = c + 'g' * (N-1)
	w, h = font.getsize(s)
	assert((w,h) == (20 * N, 42))
	img = Image.new('RGB', (w, h), (255, 255, 255))
	d = ImageDraw.Draw(img)
	d.text((0, 0),s, font=font, fill=(0, 0, 0))
	charimg = numpy.array(img).astype(numpy.float32)
	
	res = sess.run(None, {
		'loop1_nowcnt': v2arr(0,numpy.int64),
		'loop1_cond_in': v2arr(True,numpy.bool),
		'loop1_inputimg_in': charimg,
		'loop1_coeff_in': numpy.array([1 for _ in range(N)]).astype(numpy.int64),
		'loop1_loop1accum_in': v2arr(0,numpy.int64),
		'loop1_loop2cnt_in': v2arr(0,numpy.int64),
	})
	chartable[res[3][0]] = c

print('built chartable')

from z3 import *

ans = [Int("x%d" % i) for i in range(N)]
sol = Solver()

for i in range(N):
	s = 0
	for j in range(N):
		ij = (i - j + N) % N
		s += A[i*N+ij]*ans[j]
	sol.add(s == B[i])

print('construct')
print(sol.check())

mod = sol.model()
ans = ''.join(chartable[mod[c].as_long()] for c in ans)
print(ans)