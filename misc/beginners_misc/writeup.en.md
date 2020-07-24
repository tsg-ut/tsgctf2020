# Beginner's Misc Writeup En

## Problem

The challenge is given in the form of the following code.

```python
exploit = input('? ')
if eval(b64encode(exploit.encode('UTF-8'))) == math.pi:
  print(open('flag.txt').read())
```

The purpose of the problem is to come up with a UTF-8 string, which matches math.pi when encoded in Base64 and then evaluated in Python.

## Solution

In Base64, 3 characters of the original string is converted into 4 characters. Therefore, it is natural to separate every 4 characters on Base64.

So, let's think about composing the Base64 string in the following format.

![](https://i.imgur.com/9zAUSpx.jpg)

This is in the form of a huge fraction of digits that is acceptable in Python.

You can determine it from the top digit, by first looking for a Base64 string of four digits that would be valid in UTF-8, and secondly using it to determine the fraction from the left string.

If you don't adjust the number of digits in the last part, it will not be accepted when encoding with Base64, so it will be safe if you add the appropriate value which will be 0 after this.

By this method, for example, you can get the following exploit string:

```
ｶ箷ןz㍶㍿ێ|ׯvӝ<׍uӍ>㍿㍴㍴㍴㍴㍴㍴㍴㍴㍴㍴
```

and Base64 encoded one:

```python
7722566315964422442/2458169205081411040+442/4420442044204420442044204420442044204420
```

This can be evaluated in python as followings.

```python
>>> 7722566315964422442/2458169205081411040+442/4420442044204420442044204420442044204420
3.141592653589793
```

We got pi.

FYI: Golfed version.

```
㮼뎼מ;㍿׿9ێ|ӟ7׽>׍{
466864681547442/178524580583170+746/1417
```

Plus, the shortest answer sumbitted during the TSG CTF was 21 bytes.

Translated with www.DeepL.com/Translator (free version)

## Solver Script

[solve.rb](solver/solve.rb)
