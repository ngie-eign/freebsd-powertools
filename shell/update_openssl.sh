#!/bin/sh

set -eu

RELEASE_TAG=$1; shift

RELEASE_URL_BASE="https://github.com/openssl/openssl/releases/download/${RELEASE_TAG}"

SRC_TARBALL="${RELEASE_TAG}.tar.gz"
SRC_PGP_SIG="${SRC_TARBALL}.asc"
SRC_SHA256_FILE="${SRC_TARBALL}.sha256"

cd ~/git/freebsd-src/worktree/vendor
(
	cd ../
	for file in "${SRC_TARBALL}" "${SRC_PGP_SIG}" "${SRC_SHA256_FILE}"; do
		fetch "${RELEASE_URL_BASE}/${file}"
	done
	sha256 --check "${SRC_SHA256_FILE}"
	gpg --verify "${SRC_PGP_SIG}" "${SRC_TARBALL}"
	read -p 'Press enter to continue> ' j
	tar xvzf "${SRC_TARBALL}"
	cd "${RELEASE_TAG}"
	rsync -av --delete --exclude .git . ../vendor
)
(
	cd "../${RELEASE_TAG}"
	./Configure enable-fips enable-ktls threads shared --prefix=/usr
)
