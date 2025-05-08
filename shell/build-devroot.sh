#!/bin/sh
#
# usage: build-devroot.sh dev-root
#
# shellcheck shell=dash

error()
{
	printf "${0##*/}: ERROR: %s\n" "$@"
}

set -eu

DESTDIR="$1"; shift
SRCDIR="$1"; shift

export DESTDIR

if [ -d "${SRCDIR}/sys/sys/param.h" ]; then
	error "$SRCDIR not a source directory."
	exit 1
fi

make installworld
make distribution
etcupdate extract -D "$DESTDIR" -s "$SRCDIR"
