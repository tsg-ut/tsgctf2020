cd /home/user
#timeout --foreground -s 9 120s ./rachell
LD_PRELOAD=/home/user/libc.so.6 timeout --foreground -s 9 30s ./rachell
