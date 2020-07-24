#!/bin/sh

cd /home/user
LD_PRELOAD=./libc.so.6 ./detective
