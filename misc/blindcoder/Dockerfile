FROM asuri/ctf-xinetd

RUN rm -rf /etc/xinetd.d/* && \
    apt-get update && \
    apt-get -y upgrade --option=Dpkg::Options::=--force-confdef

RUN apt-get install git build-essential libffi-dev libssl-dev zlib1g-dev liblzma-dev libbz2-dev libreadline-dev libsqlite3-dev -y && \
    groupadd -r user && \
    useradd -r -g user user && \
    (curl pyenv.run | bash) && \
    ~/.pyenv/bin/pyenv init - && \
    ~/.pyenv/bin/pyenv install 3.8.3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY ./src/xinetd.conf /etc/xinetd.d/ctf
COPY ./dist /home/user/app

WORKDIR /home/user/app

RUN chmod 444 /etc/xinetd.d/ctf && \
    /root/.pyenv/shims/python -m pip install -r requirements.txt
