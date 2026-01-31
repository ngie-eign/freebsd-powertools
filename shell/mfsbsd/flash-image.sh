#!/bin/sh
#
# Automate writing flashing the most recent mfsbsd image to the first da(4)
# device.
#
# XXX: this is a really simple/hacky solution. Convert from /bin/sh to a
# python (or other high-level) language that would be more appropriate for
# interactive scripting.

newest_image=$(ls -t mfsbsd-FreeBSD_* | head -n 1)
dev=$(ls /dev/da[0-9] 2>/dev/null | head -n 1)
if [ -z "$dev" ]; then
	echo "No compatible target devices attached"
	exit
elif [ ! -c "$dev" ]; then
	echo "'$dev' is not a valid device."
	exit 1
fi
read -p "Flash $newest_image to $dev [y/N]? " yesno

bail=true
if [ -n "$yesno" ]; then
	case "$yesno" in
	""|[yY])
		bail=false
		;;
	*)
		;;
	esac
fi
if $bail; then
	echo "Exiting"
	exit 0
fi
sudo dd if="$newest_image" of=$dev bs=128m
