FROM httpd:2.4.43-alpine

ENV GOPATH=/go/src

RUN mkdir -p $GOPATH && \
    apk upgrade && \
    apk add tcpdump supervisor curl --no-cache && \
    curl -L https://github.com/Asuri-Team/ctf-xinetd/raw/master/tcpdump.sh -o /usr/local/bin/tcpdump.sh && \
    chmod +x /usr/local/bin/tcpdump.sh && \
    apk add go --repository http://dl-cdn.alpinelinux.org/alpine/edge/community

COPY dist/src/*.go /go/src/
COPY dist/data /var/lib/data

RUN cd /go/src && \
    go build -o /usr/local/apache2/cgi-bin/index.cgi

RUN echo 'Include conf.d/*.conf' >> /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/\*\*\* CENSORED \*\*\*/TSGCTF{Y0URETH3W1NNNER202OH}/' /var/lib/data/G04YFRMAW/2020-07-11.json

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]