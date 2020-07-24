#!/bin/sh

cd /home/user

#python3.7 proof-of-work.py &&
nsjail -Mo  -R /flag -R /bin/ -R /lib -R /lib64/ -R /usr/ -R /sbin/ -R /home/user/env -T /prog --keep_caps --quiet --time_limit 30 -- /home/user/env/run.sh
