#!/bin/bash
#
# From the given .log create a list of sectors to fetch again
# Name this .redo to run ./redo.sh with it


OOPS()
{
echo "OOPS: $*" >&2
exit 23
}

numeric()
{
case "$1" in
''|*[^0-9]*)	OOPS "numeric? $1"
esac
}


BLK="${1:-4096}"
while read -ru6 error offset length
do
	case "$error" in
	err)	;;
	*)	OOPS "Wrong line: $error $offset $length";;
	esac
	numeric "$offset"
	numeric "$length"
	while [ 0 -lt $length ]
	do
		let n=BLK
		[ $n -lt $length ] || let n=length
		printf "%-4s %20d %5d\n" redo "$offset" "$n"
		let offset+=BLK
		let length-=BLK
	done
done 6<"${2:-$IMAGE}.log"

