#!/bin/sh

device_file=${1:-devices.txt}

if [ "$device_file" = "-" ]; then
	trap 'rm -f $tmpfile' EXIT
	tmpfile=$(mktemp dataXXXXXX)
	cat > $tmpfile
	device_file=$tmpfile
fi

while read macaddr name; do
	name="$name" macaddr="$macaddr" ./gurl resource/dhtsensor device.json
done < $device_file
