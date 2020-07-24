import onnx,onnxruntime
import numpy as np

import params
import pickle
fontdata = pickle.load(open('fontdata','rb'))
ds = list(fontdata.items()) # (42, 20, 3)

onnx.checker.check_model(onnx.load('joined.onnx'))

m = onnxruntime.InferenceSession('joined.onnx')
for i in range(len(ds)):
	res = m.run(None,{'input': np.array(ds[i][1]).astype(np.float32)})
	print(i,res,ds[i][0])
	assert(params.S[res[0][0]] == ds[i][0])
exit()




d = onnxruntime.InferenceSession('my.onnx')
res = d.run(None,{'cond': np.array([False])})
print(res)

exit()

d = onnxruntime.InferenceSession('my.onnx')
i = np.random.rand(1).astype(np.float32)
res = d.run(None,{'i': i})
print(i,res)
