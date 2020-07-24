from PIL import Image, ImageFont, ImageDraw
import numpy
import onnxruntime

flag = input("What is the flag?> ")
assert(len(flag) == 41 and 'g' in flag)

font = ImageFont.truetype("Inconsolata-Regular.ttf", 40)
w, h = font.getsize(flag)
assert((w, h) == (20 * 41, 42))
img = Image.new('RGB', (w, h), (255, 255, 255))
ImageDraw.Draw(img).text((0, 0), flag, font=font, fill=(0, 0, 0))
flagimg = numpy.array(img).astype(numpy.float32)

print(onnxruntime.InferenceSession('problem.onnx').run(None, {'flagimg': flagimg})[0][0])
