import pythononnxproto.onnx.proto3_pb2
m = pythononnxproto.onnx.proto3_pb2.ModelProto().FromString(open('my.onnx','rb').read())
res = pythononnxproto.onnx.proto3_pb2.ModelProto().FromString(open('model_stripped.onnx','rb').read())

res.graph.input.pop()
res.graph.output.pop()

i2 = list(filter(lambda x: x[1].op_type == "Loop",enumerate(list(m.graph.node))))[0][0]
i1 = list(filter(lambda x: x[1].op_type == "Loop",enumerate(list(m.graph.node[i2].attribute[0].g.node))))[0][0]


loop1g = m.graph.node[i2].attribute[0].g.node[i1].attribute[0].g
loop1g.MergeFrom(res.graph)

name_order = [
	'const_42_20_3const', 'const_0_20_0const', 
	'loop1_cond_outconst', 'shape_1_3_20_42const', 
	'mul1', 'add1', 'slice1', 'g0', 'g1', 
	'Conv_0', 'Relu_1', 'MaxPool_2', 'Constant_3', 'Reshape_4', 'Gemm_5', 'Relu_6', 'Gemm_7',
	'h0', 'sub1', 'gat2', 'mul2', 'add2', 'ident1','ident2','ident3',
]

loop1g.node.sort(key=lambda d: name_order.index(d.name))

m.graph.node[i2].attribute[0].g.node[i1].attribute[0].g.CopyFrom(loop1g)

node_names = list(map(lambda x: x.name,m.graph.node[i2].attribute[0].g.node[i1].attribute[0].g.node))
# m.opset_import[0].version = 12
print(node_names)
assert(len(m.opset_import) == 1)
assert(m.producer_name == 'TSG')
open('joined.onnx','wb').write(m.SerializeToString())
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
