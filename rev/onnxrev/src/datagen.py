from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random,string
import numpy as np

letters = ''.join(filter(lambda c: not c in string.whitespace + ';',string.printable))
def get_random_string(length):
	return ''.join(random.choice(letters) for i in range(length))


# ((20, 42), 'y'), ((20, 43), ';')]

font = ImageFont.truetype("Inconsolata/fonts/ttf/Inconsolata-Regular.ttf", 40)


cn = {c: 0 for c in letters}
qs = {c: None for c in letters}
ds = 0
# 20 x 42
for a in range(100):
	s = get_random_string(100) + 'y'
	print(a,s)
	h,w = font.getsize(s)
	img = Image.new('RGB', (h+ds*2,w+ds*2), (255, 255, 255))
	d = ImageDraw.Draw(img)
	d.text((ds,ds),s, font=font, fill=(0, 0, 0))
	if a == 0:
		img.save('o%d.png' % a)
	v = np.array(img)
	assert(v.shape == (42 + ds*2, 20 * len(s) + ds*2, 3))
	for i,c in enumerate(s):
		if c == ' ':
			continue
		nv = v[:,i*20+ds:i*20+20+ds,]
		#nv = v[ds:-ds,i*20+ds:i*20+20+ds,]
		#print(nv.shape)
		cn[c] += 1
		if qs[c] is None:
			qs[c] = nv
		else:
			if not np.array_equal(qs[c],nv):
				print(c,i,s)
				print(qs[c].shape,nv.shape)
				assert(False)
			else:
				#print('good')
				pass

print('ok',cn)

exit()

#print(qs)
import pickle
pickle.dump(qs,open('fontdata','wb'))

exit()

ds = []
for c in letters:
	ds.append((font.getsize(c),c))
print(sorted(ds))
exit()

img.save('tes.png')

#text_width, text_height = d.textsize('Hello')
