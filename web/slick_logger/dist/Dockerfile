FROM httpd:2.4.43-alpine

ENV GOPATH=/go/src

RUN mkdir -p $GOPATH && \
    apk upgrade && \
    apk add go --repository http://dl-cdn.alpinelinux.org/alpine/edge/community

COPY src/*.go /go/src/

RUN cd /go/src && \
    go build -o /usr/local/apache2/cgi-bin/index.cgi

RUN echo 'Include conf.d/*.conf' >> /usr/local/apache2/conf/httpd.conf
