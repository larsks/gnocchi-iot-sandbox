#!/bin/sh

ARCHIVE_POLICY=archive-policy.json

while getopts 'a:' ch; do
	case $ch in
		(a)	ARCHIVE_POLICY=$OPTARG
			;;
	esac
done
shift $((OPTIND - 1))

set -e

./gurl resource_type resource-type-dhtsensor.json
./gurl archive_policy $ARCHIVE_POLICY
./gurl archive_policy_rule archive-policy-rule.json
