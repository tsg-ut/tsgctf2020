FROM node:14.5.0-alpine

COPY dist /root/app
WORKDIR /root/app

RUN apk add tcpdump supervisor curl --no-cache && \
    curl -L https://github.com/Asuri-Team/ctf-xinetd/raw/master/tcpdump.sh -o /usr/local/bin/tcpdump.sh && \
    chmod +x /usr/local/bin/tcpdump.sh && \
    sed -i 's/\*\*\* CENSORED \*\*\*/TSGCTF{Goo00o0o000o000ood_job!_you_are_rEADy_7o_do_m0re_Web}/' app.js && \
    npm install

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]
