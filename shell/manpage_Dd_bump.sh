#!/bin/sh
#
# Bump the date for a manpage to today!

manpage_path="$1"

TODAY="$(date +"%B %d, %Y")"
sed -i '' -Ee 's/^\.Dd.+/\.Dd '"$TODAY"'/g' "$manpage_path"
