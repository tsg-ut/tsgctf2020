import onnx,onnxruntime
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random,string
import numpy as np
import params

letters = ''.join(filter(lambda c: not c in string.whitespace + ';',string.printable))
def get_random_string(length):
	return ''.join(random.choice(letters) for i in range(length))

font = ImageFont.truetype("Inconsolata-Regular.ttf", 40)

s = get_random_string(params.flaglen-1) + 'y'
print('randstr',s)
h,w = font.getsize(s)
img = Image.new('RGB', (h,w), (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((0,0),s, font=font, fill=(0, 0, 0))
v = np.array(img).astype(np.float32)

print('check')
onnx.checker.check_model(onnx.load('joined.onnx'))
print('checked')
m = onnxruntime.InferenceSession('joined.onnx')
print('loaded')
res = m.run(None,{'flagimg': v})
print(res)

tr = 0
for i in range(len(s)):
	for j in range(len(s)):	
		c = s[j]
		tr += (j+1)*(i+2)*letters.index(c)
print(tr)
exit()
