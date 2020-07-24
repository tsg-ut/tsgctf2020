# Note

## Author
[@kcz146](https://twitter.com/kcz146)

### Advisors
- [@hakatashi](https://twitter.com/hakatashi)
- [@lmt_swallow](https://twitter.com/lmt_swallow)

## Problem

### Note1
What is the program you have first developed? Fizz Buzz? Prime number enumeration? ToDo app...? In my case, Note Webapp!
This time, I renovated the Note app I first developed. Implemented Note deletion feature, Note search feature... and as a hidden feature, you can put any header image you want on the top of note space!
Let's write down everything -- ToDo, Password manager master password, treasure map, dark past -- and forget them all!!

* It's just a joke, DO NOT save your credentials like master password into this terrible note app!
* FLAG Format: `TSGCTF{[0-9A-Z_]*}`

http://[ip]:18364/

---

あなたが初めて書いたプログラムってなんですか？ Fizz Buzz? 素数列挙? ToDoアプリ...? 私の場合、ノートウェブアプリです！
このたび、そんな初めて書いたノートアプリを刷新しました。ノートの削除機能、検索機能、、、そして隠し機能として、あなたの好きなヘッダ画像を表示できるようになりました！
さぁ、あなたの全てを -- ToDO, パスワードマネージャのマスターパスワード、宝の地図、黒歴史を -- ノートに書き記して、忘れてしまいましょう！！

* これはジョークです、マスターパスワードをこんなノートアプリに保存するのはやめましょうね。
* FLAG Format: `TSGCTF{[0-9A-Z_]*}`

http://[ip]:18364/


### Note2

Sorry but we found unintended solution for the problem "Note". We fixed it now.

http://[ip]:18365/

---

"Note"に非想定解を発見したため、修正しました。

http://[ip]:18365/


## How to deploy

```
$ cp _env .env
# update DOMAIN in .env

$ docker-compose up -d --build --scale worker=4
```
