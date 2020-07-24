import pythononnxproto.onnx.proto3_pb2
m = pythononnxproto.onnx.proto3_pb2.ModelProto().FromString(open('my.onnx','rb').read())
res = pythononnxproto.onnx.proto3_pb2.ModelProto().FromString(open('model.onnx','rb').read())

res.graph.input.pop()
res.graph.output.pop()
res.MergeFrom(m)
d = res.opset_import.pop()
res.opset_import.pop()
res.opset_import.append(d)

name_order = [
	'g0', 'shape_1_3_20_42const', 'g1', 
	'Conv_0', 'Relu_1', 'MaxPool_2', 'Constant_3', 'Reshape_4', 'Gemm_5', 'Relu_6', 'Gemm_7', 
	'h0',
]

res.graph.node.sort(key=lambda d: name_order.index(d.name))

node_names = list(map(lambda x: x.name,res.graph.node))
print(node_names)
assert(res.opset_import[0].version == 12)
assert(res.producer_name == 'TSG')
open('joined.onnx','wb').write(res.SerializeToString())
exit()

dg = pythononnxproto.onnx.proto3_pb2.GraphProto()
dg.name = "TSGnet"
dg.doc_string = ""



d = pythononnxproto.onnx.proto3_pb2.ModelProto()
d.ir_version = 6
d.producer_name = "TSG"
d.producer_version = "2"
d.opset_import.add().version = 9
d.domain = "FlagChecker"
d.model_version = 1
d.doc_string = ""
d.graph.CopyFrom(dg)
open('my.onnx','wb').write(d.SerializeToString())
