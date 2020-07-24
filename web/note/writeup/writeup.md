###  Analysis
Expected analysis steps

1. Read scripts
1. You find `http://host:port/?<regexp search query>#<URL>` shows
   - element with `background-image: <URL>`
   - notes only matching regexp query
1. You will try to detect whether any note matches the regexp query, by controling the content located at `<URL>`.
1. You notice that notes have "deletion button"
   - Only when any note matches the regexp query, the image of "deletion button" is fetched.
   - Hence, you'll become eager to detect whether the image of "deletion button" was fetched by the communication to `<URL>`.
1. You'll find "deletion button image" has URL with `https` scheme, and its certificate was issued by *Let's Encrypt Authority X3*.
   - Other HTTPS URLs (`https://cdnjs.cloudflare.com/...`, `https://cdn.jsdelivr.net/...`, `https://use.fontawesome.com/...`) use different certificates.
1. The Let's Encrypt certificate is an intermediate one, which is signed by root CA *DST Root CA X3*.
   - You can find the detail [here](https://letsencrypt.org/certificates/).
1. What if you present a certificate signed by Let's Encrypt without the certificate for Let's Encrypt intermediate CA signed by Root CA...?
   - Actually, Firefox has the cache for SSL certificates [citation needed] ! You can find it through experiments.


### Solution

1. You should prepare
   - one machine with a global IP such as VPS
     - If testing locally, you can use `192.168.1.100` now.
   - one DNS record that points to the global IP
     - There are several free Dynamic DNS services.
     - If testing locally, you can use `jfwioaw.hopto.org` now.
1. Get a certificate issued by *Let's Encrypt Authority X3*
   - `docker run --rm -ti -v /tmp/cert/etc:/etc/letsencrypt -v /tmp/cert/var:/var/lib/letsencrypt certbot/certbot certonly --manual --preferred-challenges http --server https://acme-v02.api.letsencrypt.org/directory -d 'example.jp'`
   - If testing locally, I prepared a cert for `jfwioaw.hopto.org` in this directory.
1. Insert a short delay before presenting the SSL certificate
   - Because you want to detect whether the certificate for "deletion image" was cached, "deletion image" fetch must precede the header image fetch.
   - `socat tcp-listen:8001,bind=0.0.0.0,fork,reuseaddr system:'sleep 1; nc 127.0.0.1 5678'` (included in solver.rb)
1. Terminate TLS using only the leaf certificate (i.e. use `cert.pem` without `chain.pem` and `fullchain.pem`)
   - `socat openssl-listen:5678,fork,reuseaddr,certificate=cert.pem,key=privkey.pem,verify=0 system:'nc 127.0.0.1 6789'` (included in solver.rb)
1. Now, you can derive the 1bit information, that is the existence of preceding "deletion image" fetch, by detecting if Firefox continues HTTP communication after SSL handshakes.
