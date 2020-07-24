#!/bin/sh

cd `dirname $0`
cd ../src
make
mv beginners_pwn ../dist/beginners_pwn
