FROM moratorium08/nsjail


RUN apt update && apt upgrade -y && apt install -y python3.7 nodejs npm xinetd iproute2
RUN groupadd -r user && useradd -r -g user user

RUN apt install -y hashcash

COPY --chown=root:user ./build/start.sh /home/user/start.sh
COPY --chown=root:user ./build/proof-of-work.py /home/user/proof-of-work.py
COPY --chown=root:root ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./build/flag flag
COPY --chown=root:user ./build/env /home/user/env

WORKDIR /home/user

RUN chmod 444 /flag && \
    chmod 555 ./start.sh && \
    chmod 555 ./proof-of-work.py && \
    chmod 444 /etc/xinetd.d/ctf


USER user
EXPOSE 30003

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
