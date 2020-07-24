FROM pypy:3.6

RUN apt update && apt -y upgrade && apt install -y xinetd

RUN apt install -y hashcash

RUN groupadd -r user && useradd -r -g user user


COPY --chown=root:user ./build/start.sh /home/user/start.sh
COPY --chown=root:root ./build/ctf.conf /etc/xinetd.d/ctf
COPY --chown=root:user ./dist /home/user/env
COPY --chown=root:user ./build/flag /home/user/env/flag
COPY --chown=root:user ./build/proof-of-work.py /home/user/env/proof-of-work.py

WORKDIR /home/user

RUN chmod 444 ./env/flag && \
    chmod 555 ./start.sh && \
    chmod 444 /etc/xinetd.d/ctf

RUN mkdir /hashcash && \
    touch /hashcash/hashdb && \
    chmod a+rwt /hashcash && \
    chmod a+rw /hashcash/hashdb

USER user
EXPOSE 30004

CMD ["xinetd","-dontfork","-f","/etc/xinetd.d/ctf"]
