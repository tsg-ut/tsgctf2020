import sys
import argparse
from PIL import Image

def bytes_to_bin(bytes):
  return ''.join("{:08b}".format(byte) for byte in bytes)

parser = argparse.ArgumentParser()
parser.add_argument('base_image')
parser.add_argument('secret_file')
parser.add_argument('-o', '--output', nargs=1)
args = parser.parse_args()

with open(args.secret_file, 'rb') as f:
  secret = bytes_to_bin(f.read())

image = Image.open(args.base_image)
w, h = image.size
assert(len(secret) <= w * h)

for y in range(h):
  for x in range(w):
    pixel = image.getpixel((x, y))

    # Let's repaint LSB :)
    if y * w + x < len(secret):
      image.putpixel((x, y), pixel ^ int(secret[y * w + x]))

image.save(args.output[0])
