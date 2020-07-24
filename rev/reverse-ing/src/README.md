```
nasm problem.s -felf64 -o problem.o && ld problem.o && strip -N key1 -N revloop -N loop -N loop2 -N ok -N end -N correct -N wrong a.out && python3 modify.py
```
でreversingができあがるので，それが問題ファイルです．
