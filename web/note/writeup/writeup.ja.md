### 道筋
想定していた道筋はこのような感じです。

1. 配布スクリプト・HTML/JavaScript/CSSを読む。
1. `http://host:port/?<RegExp検索クエリ>#<URL>` で以下が表示されることに気づく:
   - `background-image: <URL>`をstyleに持つようなHTML要素
   - RegExp検索クエリにマッチするようなノート
1. ここで、`<URL>`に配置するコンテンツをうまく用意することで、一つ以上のノートが検索クエリにマッチするかを検出したくなる。
1. ノートには、「削除用ボタン」が付属していることに気づく。
   - つまり、一つ以上のノートが検索クエリにマッチしたときのみ、「削除用ボタン」の画像がブラウザから取得されることになる。
   - クエリにマッチするノートの存在性検出が削除用ボタン画像の取得有無検出に帰着され、これを検出できるような仕組みを`<URL>`に配置したくなる。
1. 削除用ボタン画像が`https`スキームのURL上にあることに気づき、そしてそのSSL証明書が*Let's Encrypt Authority X3*によって発行されていることに気づく。
   - 他のHTTPSのURL(`https://cdnjs.cloudflare.com/...`, `https://cdn.jsdelivr.net/...`, `https://use.fontawesome.com/...`)は、どれも別の発行元からのSSL証明書を使用している。
1. Let's Encryptは証明書チェイン上中間CAであり、ルートCAである*DST Root CA X3*によって信頼されている。
   - 詳細はLet'sEncryptのサイト上に書いてある: [link](https://letsencrypt.org/certificates/).
1. もしルートCAからの署名済み証明書なしに、Let'sEncryptによって署名された証明書のみをブラウザに提示したらどうなるだろう...?
   - 実は、FirefoxはSSL証明書へのキャッシュを実装している [要出典]! これは実験によって気づくことができる。


### 解法

1. まず、次のものを準備する必要がある。
   - VPSのような、グローバルIPをもつマシン1つ
     - ここでのローカルテストだけなら、`192.168.1.100`を利用することができる。適当なマシンにこのIPを振れば良い。
   - そのグローバルIPを指すような、DNSレコード1つ
     - 無料のダイナミックDNSサービスというのが世の中には複数ある。
     - ここでのローカルテストだけなら、`jfwioaw.hopto.org`を利用することができる。`192.168.1.100`を指している。
1. *Let's Encrypt Authority X3*に署名された証明書を発行する。
   - `docker run --rm -ti -v /tmp/cert/etc:/etc/letsencrypt -v /tmp/cert/var:/var/lib/letsencrypt certbot/certbot certonly --manual --preferred-challenges http --server https://acme-v02.api.letsencrypt.org/directory -d 'example.jp'`
   - ここでのローカルテストだけなら、既に`jfwioaw.hopto.org`向けの証明書を、このディレクトリに用意してあるので、これを利用すれば良い。
1. 証明書をブラウザに提示する前に、少しの遅延を入れる。
   - 今、削除用ボタン画像の取得が過去にあったかどうかでノート検出をしたいのだから、画像の取得は(もし行われるのであれば)ヘッダ画像の取得に対し先行している必要がある。
   - `socat tcp-listen:8001,bind=0.0.0.0,fork,reuseaddr system:'sleep 1; nc 127.0.0.1 5678'` (solver.rb内に含まれている)
1. TLSを葉となる証明書のみを使って終端する。つまり、certbotによって保存されるもののうち、`cert.pem`のみを使って、`chain.pem`と`fullchain.pem`は使わない。
   - `socat openssl-listen:5678,fork,reuseaddr,certificate=cert.pem,key=privkey.pem,verify=0 system:'nc 127.0.0.1 6789'` (solver.rb内に含まれている)
1. 以上によって、FirefoxがSSLハンドシェイク後にHTTP通信を継続するかを調べることで、削除用ボタン画像取得が行われたかどうかという1bitの情報を得ることができる。
