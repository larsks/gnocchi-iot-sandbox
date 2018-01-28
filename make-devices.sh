#!/bin/sh

while read macaddr name; do
	name="$name" macaddr="$macaddr" ./gurl resource/dhtsensor device.json
done < devices.txt
