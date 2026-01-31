#!/bin/sh
#
# Run `make tinderbox`.
#
# Based on instructions in /etc/motd .

USERTMP="/scratch/tmp/$USER"
SRCDIR="$USERTMP/src"
export MAKEOBJDIRPREFIX="$USERTMP/obj"
rm -f "$SRCDIR/_."*
: ${MAKE_JOBS=$(( $(nproc || sysctl -n kern.smp.ncpus) / 3 ))}

make -s -j"${MAKE_JOBS}" __MAKE_CONF=/dev/null tinderbox "$@"
