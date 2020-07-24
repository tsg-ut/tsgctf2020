# First, compile compiler_exploit.x with the following command.
# `python3 interpreter.py compiler.x < compiler_exploit.x > tmp.s`
# Then, run this script, and you get "exploit.s", which is an answer for this problem.


s = open('tmp.s').read()
head = s[:s.index('[123,456,789]')]
tail = s[s.index('[314,159,265]')+len('[314,159,265]'):]
headstr = ''.join(str(list(map(lambda x: ord(x),head))).split(' '))
tailstr = ''.join(str(list(map(lambda x: ord(x),tail))).split(' '))
exploit = s.replace('[123,456,789]',headstr).replace('[314,159,265]',tailstr)
open('exploit.s','w').write(exploit)