from base64 import b64encode
import math

exploit = input('? ')
if eval(b64encode(exploit.encode('UTF-8'))) == math.pi:
  print(open('flag.txt').read())
