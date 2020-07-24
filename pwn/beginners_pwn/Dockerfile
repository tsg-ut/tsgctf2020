FROM ubuntu:20.04


RUN apt-get update && \
        apt-get -y upgrade && \
        apt-get install -y \
            xinetd \
            iproute2

RUN groupadd -r user && useradd -r -g user user

COPY --chown=root:user ./build/start.sh /home/user/start.sh
COPY --chown=root:root ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./build/flag /home/user/flag
COPY --chown=root:user ./dist/beginners_pwn /home/user/beginners_pwn

WORKDIR /home/user

RUN chmod 444 ./flag && \
    chmod 555 ./beginners_pwn && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

USER user
EXPOSE 30002

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
