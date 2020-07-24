#!/bin/sh

gcc -Wl,-z,relro,-z,now -no-pie -o ../dist/karte karte.c
