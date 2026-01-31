#!/bin/sh

set -ex

cd "$(dirname "$0")"

: ${MK_CLEAN=yes}

export KERNCONF=NGIE_MAC
export KERNCONFDIR="$PWD"
export PORTSDIR="$(realpath ~ngie/git/freebsd-ports)"
export SRC_DIR="$(realpath ~ngie/git/freebsd-src/worktree/main)"
export MFSROOT_MAXSIZE=1g
export NO_PACKAGES=1
crypto_MODULES="aesni crypto cryptodev"
ure_MODULES="usb/uether usb/ure"
wlan_MODULES="wlan wlan_tkip"
export CFLAGS="-DASMC_DEBUG"
MODULES="asmc ${crypto_MODULES} nullfs opensolaris rge tmpfs ${ure_MODULES} ${wlan_MODULES}"

export MFSMODULES="$(echo "${MODULES}" | tr ' ' '\n' | xargs -n 1 basename | tr '\n' ' ' | sed -e 's/ure/if_ure/')"
export MODULES_OVERRIDE="${MODULES}"

sh "${SRC_DIR}/sys/conf/newvers.sh"
export RELEASE="$(what -sq vers.c | awk '{ sub(/:$/, "", $4); print $1 "_" $4 }')"
rm -f vers.c version

#make_debug_flags="-d lv"
script build.ts \
    sudo -E env \
	 __MAKE_CONF=/dev/null \
	 PORTSDIR=${PORTSDIR} \
	 SRCCONF="${PWD}/src.conf" \
	 MFSMODULES="${MFSMODULES}" \
	 MODULES_OVERRIDE="${MODULES_OVERRIDE}" \
	 MK_CLEAN=${MK_CLEAN} \
	 SRC_DIR="${SRC_DIR}" \
	 make ${make_debug_flags} image \
	 -DCUSTOM -DBUILDKERNEL -DBUILDWORLD MAKEJOBS=16
