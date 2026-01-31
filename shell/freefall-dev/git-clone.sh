#!/bin/sh
#
# Clone repo from local cache.
#
# Based on instructions in /etc/motd .

USERTMP="/scratch/tmp/$USER"
SRCDIR="$USERTMP/src"

git clone --reference /home/git/src.git https://git.freebsd.org/src.git \
    "$SRCDIR"
