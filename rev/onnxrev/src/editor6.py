import onnx
from onnx import helper
from onnx import AttributeProto, TensorProto, GraphProto

import numpy as np
import params

flag = 'a' * params.flaglen


regnode = []

regcount = ''
def resetregnode():
	global regnode,regcount
	regnode = []
	regcount += '_'

def genconst(na,ty,v):
	global regnode,regcount
	na = regcount + na
	no = onnx.helper.make_node(
    'Constant',
    name = na + 'const',
    inputs=[],
    outputs=[na],
    value=onnx.helper.make_tensor(
        name= na + 'const',
        data_type=ty,
        dims=v.shape,
        vals=v,
		)
	)
	regnode.append(no)
	return helper.make_tensor_value_info(na, ty, v.shape)


def genconlist(v):
	genconst('const_%s' % '_'.join(map(str,v)),TensorProto.INT64,np.array(v,dtype=np.int64))

genconst('shape_1_3_20_42',TensorProto.INT64,np.array([1,3,20,42],dtype=np.int64))

genconst('loop1_cond_out',TensorProto.BOOL,np.array([True],dtype=np.bool))

regnode.append(onnx.helper.make_node(
        'Transpose',
        name = 'g0',
        inputs=['input'],   # 42,20,3
        outputs=['beftob'], # 3,20,42
        perm=[2,1,0]
))

regnode.append(onnx.helper.make_node(
	'Reshape',
	name = 'g1',
	inputs=['beftob','shape_1_3_20_42'],
	outputs=['img'],
))


# helper.make_tensor_value_info('class', TensorProto.FLOAT, [1,93])
# class :: 1,93

regnode.append(onnx.helper.make_node(
	'ArgMax',
	name = 'h0',
	inputs=['class'],
	outputs=['result'],
	keepdims=0,
	axis=1
))


regnode.append(onnx.helper.make_node(
    'Sub',
    name='sub1',
    inputs=['loop1_loop2cnt_in','loop1_nowcnt'],
    outputs=['loop1_nowcnt_subed'],
))

regnode.append(onnx.helper.make_node(
    'Gather',
    name='gat2',
    inputs=['loop1_coeff_in', 'loop1_nowcnt_subed'],
    outputs=['loop1_coeff_in_indexed'],
))


regnode.append(onnx.helper.make_node(
    'Mul',
    name='mul2',
    inputs=['result', 'loop1_coeff_in_indexed'],
    outputs=['loop1tmp1'],
))

regnode.append(onnx.helper.make_node(
    'Add',
    name='add2',
    inputs=['loop1tmp1', 'loop1_loop1accum_in'],
    outputs=['loop1_loop1accum_out'],
))

regnode.append(onnx.helper.make_node(
    'Mul',
    name='mul1',
    inputs=['loop1_nowcnt', 'const_0_20_0'],
    outputs=['loop1_slicestart'],
))

regnode.append(onnx.helper.make_node(
    'Add',
    name='add1',
    inputs=['loop1_slicestart', 'const_42_20_3'],
    outputs=['loop1_sliceend'],
))

regnode.append(onnx.helper.make_node(
    'Slice',
    name='slice1',
    inputs=['loop1_inputimg_in', 'loop1_slicestart', 'loop1_sliceend'],
    outputs=['input'],
))


regnode.append(onnx.helper.make_node(
    'Identity',
    name='ident1',
    inputs=['loop1_inputimg_in'],
    outputs=['loop1_inputimg_out'],
))

regnode.append(onnx.helper.make_node(
    'Identity',
    name='ident2',
    inputs=['loop1_coeff_in'],
    outputs=['loop1_coeff_out'],
))

regnode.append(onnx.helper.make_node(
    'Identity',
    name='ident3',
    inputs=['loop1_loop2cnt_in'],
    outputs=['loop1_loop2cnt_out'],
))

genconlist([42,20,3])
genconlist([0,20,0])

loop1graph = helper.make_graph(
    regnode,
    'loop1',
    [
    	helper.make_tensor_value_info('loop1_nowcnt', TensorProto.INT64, [1]),
    	helper.make_tensor_value_info('loop1_cond_in', TensorProto.BOOL, [1]),
    	helper.make_tensor_value_info('loop1_inputimg_in', TensorProto.FLOAT, [42,20 * len(flag),3]),
    	helper.make_tensor_value_info('loop1_coeff_in', TensorProto.INT64, [len(flag)]),
    	helper.make_tensor_value_info('loop1_loop1accum_in', TensorProto.INT64, [1]),
    	helper.make_tensor_value_info('loop1_loop2cnt_in', TensorProto.INT64, [1]),
    ],
    [
    	helper.make_tensor_value_info('loop1_cond_out', TensorProto.BOOL, [1]),
    	helper.make_tensor_value_info('loop1_inputimg_out', TensorProto.FLOAT, [42,20 * len(flag),3]),
    	helper.make_tensor_value_info('loop1_coeff_out', TensorProto.INT64, [len(flag)]),
    	helper.make_tensor_value_info('loop1_loop1accum_out', TensorProto.INT64, [1]),
    	helper.make_tensor_value_info('loop1_loop2cnt_out', TensorProto.INT64, [1]),
    ],
)

resetregnode()

genconst('const_0',TensorProto.INT64,np.array([0],dtype=np.int64))
genconst('const_len_flag',TensorProto.INT64,np.array([len(flag)],dtype=np.int64))
genconst('const_true',TensorProto.BOOL,np.array([True],dtype=np.bool))
genconst('loop2_cond_out',TensorProto.BOOL,np.array([True],dtype=np.bool))
genconlist([len(flag)])

regnode.append(onnx.helper.make_node(
    'Gather',
    name='gat2_2',
    inputs=['loop2_coeff_in', 'loop2_nowcnt'],
    outputs=['loop2_coeff_in_indexed_befrs'],
))

regnode.append(onnx.helper.make_node(
	'Reshape',
	name = 'lasr2',
	inputs=['loop2_coeff_in_indexed_befrs','_const_%d' % len(flag)],
	outputs=['loop2_coeff_in_indexed'],
))

regnode.append(onnx.helper.make_node(
	'Loop',
	body = loop1graph,
	name = 'loopnode1',
	inputs=['_const_len_flag','_const_true','loop2_inputimg_in','loop2_coeff_in_indexed','_const_0', 'loop2_nowcnt'],
	outputs=['loop2_inputimg_out','loop1_coeff_out_dummy','loop1result','loop1_loop2cnt_out_dummy'],
))

regnode.append(onnx.helper.make_node(
    'Gather',
    name='gat3_2',
    inputs=['loop2_targ_in', 'loop2_nowcnt'],
    outputs=['loop2_targ_in_indexed'],
))

regnode.append(onnx.helper.make_node(
    'Equal',
    name='eq1_2',
    inputs=['loop2_targ_in_indexed', 'loop1result'],
    outputs=['loop2_cmpres'],
))

regnode.append(onnx.helper.make_node(
    'And',
    name='and1_2',
    inputs=['loop2_cmpres', 'loop2_accum_in'],
    outputs=['loop2_accum_out'],
))

regnode.append(onnx.helper.make_node(
    'Identity',
    name='ident2_2',
    inputs=['loop2_coeff_in'],
    outputs=['loop2_coeff_out'],
))

regnode.append(onnx.helper.make_node(
    'Identity',
    name='ident3_2',
    inputs=['loop2_targ_in'],
    outputs=['loop2_targ_out'],
))

loop2graph = helper.make_graph(
    regnode,
    'loop2',
    [
    	helper.make_tensor_value_info('loop2_nowcnt', TensorProto.INT64, [1]),
    	helper.make_tensor_value_info('loop2_cond_in', TensorProto.BOOL, [1]),
    	helper.make_tensor_value_info('loop2_inputimg_in', TensorProto.FLOAT, [42,20 * len(flag),3]),
    	helper.make_tensor_value_info('loop2_coeff_in', TensorProto.INT64, [len(flag),len(flag)]),
    	#helper.make_tensor_value_info('loop2_coeff_in', TensorProto.INT64, [len(flag)]),
    	helper.make_tensor_value_info('loop2_targ_in', TensorProto.INT64, [len(flag)]),
    	helper.make_tensor_value_info('loop2_accum_in', TensorProto.BOOL, [1]),
    ],
    [
    	helper.make_tensor_value_info('_loop2_cond_out', TensorProto.BOOL, [1]),
    	helper.make_tensor_value_info('loop2_inputimg_out', TensorProto.FLOAT, [42,20 * len(flag),3]),
    	helper.make_tensor_value_info('loop2_coeff_out', TensorProto.INT64, [len(flag),len(flag)]),
    	#helper.make_tensor_value_info('loop2_coeff_out', TensorProto.INT64, [len(flag)]),
    	helper.make_tensor_value_info('loop2_targ_out', TensorProto.INT64, [len(flag)]),
    	helper.make_tensor_value_info('loop2_accum_out', TensorProto.BOOL, [1]),
    ],
)

resetregnode()

import params
coeff = params.A
targ = params.B

genconst('const_true',TensorProto.BOOL,np.array([True],dtype=np.int64))
genconst('const_len_flag',TensorProto.INT64,np.array([len(flag)],dtype=np.int64))
genconst('targ_in',TensorProto.INT64,np.array(targ,dtype=np.int64))

#coeff = [[(j+2) * (i+1) for i in range(len(flag))] for j in range(len(flag))]

coeff = np.array(coeff,dtype=np.int64)
# genconst('coeff_in_base',TensorProto.INT64,np.array(coeff,dtype=np.int64))
regnode.append(onnx.helper.make_node(
    'Constant',
    inputs=[],
    outputs=['__coeff_in'],
    value=onnx.helper.make_tensor(
        name='const_tensor',
        data_type=onnx.TensorProto.INT64,
        dims=coeff.shape,
        vals=coeff.flatten().astype(np.int64),
    ),
))

#genconst('const_true',TensorProto.BOOL,np.array([True],dtype=np.bool))

"""
genconlist([len(flag),len(flag)])
regnode.append(onnx.helper.make_node(
	'Reshape',
	name = 'resx',
	inputs=['__coeff_in_base','__const_%d_%d' % (len(flag),len(flag))],
	outputs=['__coeff_in'],
))
"""

regnode.append(onnx.helper.make_node(
	'Loop',
	body = loop2graph,
	name = 'loopnode2',
	inputs=['__const_len_flag','__const_true','flagimg','__coeff_in','__targ_in','__const_true'],
	outputs=['inputimg_out','coeff_out','targ_out','loop2accum_out'],
))



genconst('correct',TensorProto.STRING,np.array([b'Correct!']))
genconst('wrong',TensorProto.STRING,np.array([b'Wrong...']))

regnode.append(onnx.helper.make_node(
    'Where',
    inputs=['loop2accum_out', '__correct', '__wrong'],
    outputs=['finalans'],
))

g = helper.make_graph(
    regnode,
    'FlagChecker',
    [helper.make_tensor_value_info('flagimg', TensorProto.FLOAT, [42,20 * len(flag),3])],
    [helper.make_tensor_value_info('finalans', TensorProto.STRING, [1])],
)

model = helper.make_model(g)
model.producer_name = 'TSG'
print(model)
#onnx.checker.check_model(model)
open('my.onnx','wb').write(model.SerializeToString())

exit()
