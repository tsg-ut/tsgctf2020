# std::vector (5 solves)

Author: @moratorium08

Estimated difficulty: medium-hard


### Outline of the program

The given python library is an std::vector wrapper. It can be used like as
follows:

```
import stdvec

l = stdvec.StdVec()

for i in range(1000):
    l.append(i)

for i in range(l.size()):
    l.set(i, l.get(i) + 1)

s = 0
for x in l:
    s += x

print(s == sum(range(1001)))
```
The output of this program is True.

As you can see from the above program, this library can
- create a zero-length std::vector
- append an object to the vector
- set/get an element at n-th.
- iterate over the vector


### Vulnerability

The vulnerability is 'iterator invalidation.'

```
$ cat bad.py
import stdvec
l = stdvec.StdVec()
for i in range(256):
    l.append(0xdeadbeef)
for i in l:
    l.append(1)
    print(i)
print(l)
$ /usr/bin/python3.7 bad.py
3735928559
Segmentation fault (core dumped)
```

We take a closer look at why this bug happens.

Focus on the implementation of `iter`.

```
static PyObject*
iter(StdVec *self, PyObject *args){
    vector<PyObject *>::iterator st = self->v->begin();
    vector<PyObject *>::iterator ed = self->v->end();
    StdVecIter *itr = PyObject_New(StdVecIter, &StdVecIterType);
    itr->current = st;
    itr->end = ed;
    return (PyObject *)itr;
}
```

In this implementation, the object of type StdVecIter holds the iterator of a given vector.
The iterator is implemented by the pointer to the internal buffer of the vector.

Remember that std::vector reallocates the internal buffer when the buffer has no more capacity to append a new object, which means that the internal buffer could be freed when `append` is called.
<strong>This is the bad situation.</strong>
In the above example, we iterate over l in the second for-loop. Then, in the loop, we append `1` to l.
The size of the internal buffer of std::vec is implemented to be the power of 2. Therefore, the append of the first loop will cause free of the current buffer. However, we iterated over the old buffer, and we have the pointer to that. <strong>UAF!!</strong>


### Fake Object

By using iterator invalidation trick,
we can get the pointer to the buffer which has already been freed.
The next thing we want to do is to fake the buffer, and get AAW/AAR.

`bytearray` is useful for this situation. `bytearray` is also one of the PyObjects, and it internally has the size and the pointer to the buffer, bytearray. Therefore, if you create a bytearray such that the address is 0, and the size is INT_MAX, you can do AAW/AAR.
So, the next goal is to get this fake bytearray object.

This is just a kind of heap feng shui. A small tip is that the allocator of Python uses their own allocator for the objects smaller than 512 bytes. Therefore, to create the fake buffer, we have to use a little big buffer.

After that, you can do almost everything.
libc address can be leaked from GOT. You can overwrite `free_hook,` and free the buffer starts from `/bin/sh\x00`,
which leads to getting the shell!

POC: [solver/solve2.py](solver/solve2.py)




