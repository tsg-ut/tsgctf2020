import pythononnxproto.onnx.proto3_pb2
res = pythononnxproto.onnx.proto3_pb2.ModelProto().FromString(open('model.onnx','rb').read())

"""
trs = list(res.graph.initializer)
while len(res.graph.initializer) > 0:
	res.graph.initializer.pop()
for d in trs:
	if d.name == "param0" or d.name == "param1":
		continue
	res.graph.initializer.append(d)
"""

res.graph.name = "X"

open('model_stripped.onnx','wb').write(res.SerializeToString())
