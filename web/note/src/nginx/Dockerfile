FROM nginx

RUN apt-get update -y && \
    apt-get install tcpdump supervisor curl -y && \
    curl -L https://github.com/Asuri-Team/ctf-xinetd/raw/master/tcpdump.sh -o /usr/local/bin/tcpdump.sh && \
    chmod +x /usr/local/bin/tcpdump.sh

CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisord.conf" ]
