# ONNXrev

## How to solve

First, you need to examine 
the network `problem.onnx` by visualizing or printing it.
This network works according to the following algorithm, where `oracle` is 
a combination of some neural network modules.

```python
img = drawing_text(flag)
# img.shape == (42, 20 * 41, 3)
ok = True
for i in range(41):
  s = 0
  for j in range(41):
    c = oracle(numpy.transpose(img[:,j*20:j*20+20,:],(2,1,0)))
    s += c * coeff[i][i-j]
  ok = ok and s == target[i]
print('Correct!' if ok else 'Wrong...')
```

By using `coeff` and `target` arrays,
you can obtain a array `ans`, whose jth value is the value 
`oracle(numpy.transpose(img[:,j*20:j*20+20,:],(2,1,0)))` should be
 to output "Correct!".
`Inconsolata-Regular.ttf` is a monospaced font, and 
the array `img[:,j*20:j*20+20,:]` corresponds to the image of the jth character of the flag.
By calculating the return value of 
`oracle`
for each printable characters and comparing 
the return values with the array `ans`, you can finally get the correct flag.

The intended solution is available at [./solver/](solver).
## Flag

`TSGCTF{OnNx_1s_4_kiNd_0f_e5oL4ng_I_7hink}`
