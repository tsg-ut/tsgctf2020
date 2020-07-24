import re
from sage.modules.free_module_integer import IntegerLattice
from math import sqrt, cos, pi
from PIL import Image


# Restore ZZs of original JPEG

qt = [
  16,  11,  10,  16,  24,  40,  51,  61,
  12,  12,  14,  19,  26,  58,  60,  55,
  14,  13,  16,  24,  40,  57,  69,  56,
  14,  17,  22,  29,  51,  87,  80,  62,
  18,  22,  37,  56,  68, 109, 103,  77,
  24,  35,  55,  64,  81, 104, 113,  92,
  49,  64,  78,  87, 103, 121, 120, 101,
  72,  92,  95,  98, 112, 100, 103,  99,
]

# Babai's Nearest Plane algorithm
# from: http://mslc.ctf.su/wp/plaidctf-2016-sexec-crypto-300/
def Babai_closest_vector(M, G, target):
  small = target
  for _ in range(1):
    for i in reversed(range(M.nrows())):
      c = ((small * G[i]) / (G[i] * G[i])).round()
      small -= M[i] * c
  return target - small

vectors = []
for u in range(8):
  for v in range(8):
    vec = [0] * 64
    vec[v * 8 + u] = 1
    for y in range(8):
      for x in range(8):
        if u == 0:
          cu = sqrt(1 / 2)
        else:
          cu = 1

        if v == 0:
          cv = sqrt(1 / 2)
        else:
          cv = 1

        a = cos((2 * x + 1) * u / 16 * pi)
        b = cos((2 * y + 1) * v / 16 * pi)
        vec.append(int(cu * cv * qt[v * 8 + u] * a * b / 4 * (2 ** 32)))
    vectors.append(vec)

lattice = IntegerLattice(vectors, lll_reduce=True)
gram = lattice.reduced_basis.gram_schmidt()[0]
print("LLL done")

image = Image.open('../dist/output.png')
pixels = list(image.getdata())

zzs = []
for by in range(128 // 8):
  for bx in range(128 // 8):
    print((bx, by))
    ans = [0] * 64
    tg = [128] * 64

    for ay in range(8):
      for ax in range(8):
        x = bx * 8 + ax
        y = by * 8 + ay
        ans.append((pixels[y * 128 + x] - 128) * (2 ** 32))
        tg.append(pixels[y * 128 + x])

    target = vector(ZZ, ans)
    res = Babai_closest_vector(lattice.reduced_basis, gram, target)
    zzs.append(list([int(v) for v in res[0:64]]))


# Restore exact pixels from ZZs

zig_zag = [
   0,
   1,  8,
  16,  9,  2,
   3, 10, 17, 24,
  32, 25, 18, 11, 4,
   5, 12, 19, 26, 33, 40,
  48, 41, 34, 27, 20, 13,  6,
   7, 14, 21, 28, 35, 42, 49, 56,
  57, 50, 43, 36, 29, 22, 15,
  23, 30, 37, 44, 51, 58,
  59, 52, 45, 38, 31,
  39, 46, 53, 60,
  61, 54, 47,
  55, 62,
  63
]

def number_to_ssss(number):
  ssss = abs(int(number)).bit_length()
  if number > 0:
    bits = "{:b}".format(number).rjust(ssss, '0')
  elif number < 0:
    bits = "{:b}".format(number + 2 ** ssss - 1).rjust(ssss, '0')
  else:
    bits = ""
  return ssss, bits

# These can be obtained from imagemagick command described in build.sh
SOI = "FF D8"
APP0 = """
  FF E0
  00 10 4A 46 49 46 00 01
  01 00 00 01 00 01 00 00
"""
DQT = """
  FF DB
  00 43 00 10 0B 0C 0E 0C
  0A 10 0E 0D 0E 12 11 10
  13 18 28 1A 18 16 16 18
  31 23 25 1D 28 3A 33 3D
  3C 39 33 38 37 40 48 5C
  4E 40 44 57 45 37 38 50
  6D 51 57 5F 62 67 68 67
  3E 4D 71 79 70 64 78 5C
  65 67 63
"""
SOF0 = """
  FF C0
  00 0B 08 00 80 00 80 01
  01 11 00
"""
SOS = """
  FF DA
  00 08 01 01 00 00 3F 00
"""
EOI = "FF D9"

DHT_dc = ""
for i in range(16):
  DHT_dc += "{:02x}".format(12 if i == 7 else 0)
for i in range(12):
  DHT_dc += "{:02x}".format(i)
DHT_dc = "FF C4 {:04x} 00 {}".format(len(DHT_dc) // 2 + 3, DHT_dc)

DHT_ac = ""
for i in range(16):
  DHT_ac += "{:02x}".format(255 if i == 7 else 0)
for i in range(255):
  DHT_ac += "{:02x}".format(i)
DHT_ac = "FF C4 {:04x} 10 {}".format(len(DHT_ac) // 2 + 3, DHT_ac)

ECS = ""

prev_dc = 0
for zz in zzs:
  ssss, bits = number_to_ssss(zz[0] - prev_dc)
  prev_dc = zz[0]
  ECS += "{:08b}".format(ssss)
  ECS += bits

  rrrr = 0
  for i in zig_zag[1:]:
    if zz[i] == 0:
      rrrr += 1
      if rrrr == 16:
        rrrr = 0
        ECS += "11110000" # ZRL
    else:
      ssss, bits = number_to_ssss(zz[i])
      ECS += "{:04b}{:04b}".format(rrrr, ssss)
      ECS += bits
      rrrr = 0
  if rrrr > 0:
    ECS += "00000000" # EOB

# padding
ECS += "0" * (-len(ECS) % 8)

with open('restored.jpg', 'wb') as f:
  f.write(bytes.fromhex(re.sub(r'\s', '', SOI)))
  f.write(bytes.fromhex(re.sub(r'\s', '', APP0)))
  f.write(bytes.fromhex(re.sub(r'\s', '', DQT)))
  f.write(bytes.fromhex(re.sub(r'\s', '', SOF0)))
  f.write(bytes.fromhex(re.sub(r'\s', '', DHT_dc)))
  f.write(bytes.fromhex(re.sub(r'\s', '', DHT_ac)))
  f.write(bytes.fromhex(re.sub(r'\s', '', SOS)))
  f.write(bytes(int(ECS[i : i + 8], 2) for i in range(0, len(ECS), 8)))
  f.write(bytes.fromhex(re.sub(r'\s', '', EOI)))


# Restore secret.zip

stego = Image.open('../dist/output.png')
restored = Image.open('restored.jpg')
flag = ''
w, h = stego.size
for y in range(h):
  for x in range(w):
    pixel0 = stego.getpixel((x, y))
    pixel1 = restored.getpixel((x, y))
    flag += str(pixel0 ^^ pixel1)

with open('secret.zip', 'wb') as f:
  f.write(bytes(int(flag[i : i + 8], 2) for i in range(0, len(flag), 8)))