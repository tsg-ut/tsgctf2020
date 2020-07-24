import onnx
from onnx import helper
from onnx import AttributeProto, TensorProto, GraphProto

import numpy as np


def genconst(na,ty,v):
	no = onnx.helper.make_node(
    'Constant',
    name = na + 'const',
    inputs=[],
    outputs=[na],
    value=onnx.helper.make_tensor(
        name=na + 'const',
        data_type=ty,
        dims=v.shape,
        vals=v,
		)
	)
	ts = helper.make_tensor_value_info(na, ty, v.shape)
	return no,ts

shapeconst,_ = genconst('shape_1_3_20_42',TensorProto.INT64,np.array([1,3,20,42],dtype=np.int64))

trans = onnx.helper.make_node(
        'Transpose',
        name = 'g0',
        inputs=['input'],   # 42,20,3
        outputs=['beftob'], # 3,20,42
        perm=[2,1,0]
)

tobatch = onnx.helper.make_node(
	'Reshape',
	name = 'g1',
	inputs=['beftob','shape_1_3_20_42'],
	outputs=['img'],
)


# helper.make_tensor_value_info('class', TensorProto.FLOAT, [1,93])
# class :: 1,93

argmax = onnx.helper.make_node(
	'ArgMax',
	name = 'h0',
	inputs=['class'],
	outputs=['result'],
	keepdims=0,
	axis=1
)

g = helper.make_graph(
    [trans,shapeconst,tobatch,argmax],
    'FlagChecker',
    [helper.make_tensor_value_info('input', TensorProto.FLOAT, [42,20,3])],
    [helper.make_tensor_value_info('result', TensorProto.INT64, [1])],
)

model = helper.make_model(g)
model.producer_name = 'TSG'
print(model)
#onnx.checker.check_model(model)
open('my.onnx','wb').write(model.SerializeToString())

exit()




wrong = onnx.helper.make_node(
    'Constant',
    inputs=[],
    outputs=['wrong'],
    value=onnx.helper.make_tensor(
        name='wrongconst',
        data_type=onnx.TensorProto.STRING,
        dims=(1,),
        vals=[b'Wrong'],
	)
)

cv = helper.make_tensor_value_info('correct', TensorProto.STRING, [1])
wv = helper.make_tensor_value_info('wrong', TensorProto.STRING, [1])

judge = onnx.helper.make_node(
    'Where',
    inputs=['cond', 'correct', 'wrong'],
    outputs=['result'],
)

g = helper.make_graph(
    [correct,wrong,judge],
    'FlagChecker',
    [helper.make_tensor_value_info('cond', TensorProto.BOOL, [1])],
    [helper.make_tensor_value_info('result', TensorProto.STRING, [1])],
)

model = helper.make_model(g)
print(model)
onnx.checker.check_model(model)
open('my.onnx','wb').write(model.SerializeToString())

exit()



correct = onnx.helper.make_node(
    'Constant',
    inputs=[],
    outputs=['correct'],
    value=onnx.helper.make_tensor(
        name='ct1',
        data_type=onnx.TensorProto.STRING,
        dims=(1,),
        vals=[b'Correct'],
	)
)



cv = helper.make_tensor_value_info('correct', TensorProto.STRING, [1])
wv = helper.make_tensor_value_info('wrong', TensorProto.STRING, [1])

half = onnx.helper.make_node(
    'Constant',
    inputs=[],
    outputs=['half'],
    value=onnx.helper.make_tensor(
        name='const_tensor',
        data_type=onnx.TensorProto.FLOAT,
        dims=(1,),
        vals=[0.5],
	)
)

great = onnx.helper.make_node(
    'Greater',
    inputs=['i', 'half'],
    outputs=['x'],
)

x = helper.make_tensor_value_info('x', TensorProto.BOOL, [1])
node = onnx.helper.make_node(
    'If',
    inputs=['x'],
    outputs=['result'],
    then_branch=helper.make_graph(
		  [correct],
		  'then',
		  [],
		  [cv],
		),
    else_branch=helper.make_graph(
		  [wrong],
		  'else',
		  [],
		  [wv],
		),
)


g = helper.make_graph(
    [node],
    'FlagChecker',
    [x],
    [helper.make_tensor_value_info('result', TensorProto.STRING, [1])],
)

"""
g = helper.make_graph(
    [half,great,node],
    'FlagChecker',
    [helper.make_tensor_value_info('i', TensorProto.FLOAT, [1])],
    [helper.make_tensor_value_info('result', TensorProto.STRING, [1])],
)
"""

model = helper.make_model(g)
print(model)
onnx.checker.check_model(model)
open('my.onnx','wb').write(model.SerializeToString())
