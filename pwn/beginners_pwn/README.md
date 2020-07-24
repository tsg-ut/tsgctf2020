# Beginner's Pwn
## Author

@moratorium08

TODO: Replace `IPADDR` by the actual address!

```
IPADDR 30002
```

## Description


This chal is truly typical but perhaps not immediate, is it?

Hint for beginners:
On the remote server, the program runs.
Let's connect to the server by `nc IPADDR 30002`
The goal of this chal is to execute `/bin/sh` to
get the access to the remote server.
After that, you can find a flag file in the server.
Read it, please.

How to get the shell:
If you hardly know pwning techniques,
it will be a good starting point to search the following words on the Internet.

- Format String Bug
- GOT (Global Offset Table) Overwrite
- Buffer Overflow
- Return Oriented Programming
- sigreturn syscall

In my opinion, the techniques above are enough for you to solve this chal.
(In fact, some of them are required.)
Of course, you have to do trial and error.
I think this trial and error part is the most interesting part for
pwning challs. Have a fun!

Note that I think it is difficult to solve this chal
just by one line code.
I recommend you to write a solver script.
I attached a template for solver scripts with pwntools.
Feel free to use it.


かなり典型的な問題ですが、それほど直ちに解けるというわけでもないんじゃないでしょうか

初心者向けのヒント：
リモートのサーバー上で、プログラムが動いています。
`nc IPADDR 30002`によって接続してみてください。
この問題の目標は、リモートサーバーへのアクセスをするために、
`/bin/sh`を実行することです。
接続ができたら、サーバーにフラグファイルがあるのが分かると思います。
それを読んでください。

シェルをとる方法：
もしあなたがほとんどpwnの手法を知らないならば、
次の単語をインターネットで調べることは、良いとっかかりになると思います。

- Format String Bug
- GOT (Global Offset Table) Overwrite
- Buffer Overflow
- Return Oriented Programming
- sigreturn syscall
- etc.

私の意見では、この問題を解くためには、上述した手法で事足りると思います。
（実際のところ、これらのうちのいくつかが必要です）
もちろん、試行錯誤は必要です。この試行錯誤をするのが
pwn問題の一番面白いところだと思います。楽しんでください。

注意ですが、この問題はワンライナーで解くのは難しいと思われます。
ソルバースクリプトを書くことをおすすめします。
pwntoolsを使ったソルバスクリプトのテンプレートも添付しました。
ご自由にお使いください。


* [beginners_pwn](dist/beginners_pwn)
* [solver_template.py](dist/solver.py)

## Estimated Difficulty

beginners
