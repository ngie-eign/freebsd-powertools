#!/bin/sh
#
# For doing "make tinderbox" on FreeBSD hosts.

: "${USERTMP="/scratch/tmp/$USER"}"
SRCDIR="$USERTMP/src"
export MAKEOBJDIRPREFIX="$USERTMP/obj"
rm -f "$SRCDIR"/_.*

make -s -j8 __MAKE_CONF=/dev/null tinderbox "$@"
