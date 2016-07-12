#!/bin/bash
#
# Redo some sectors prepared in IMAGE.redo
# Prepare with
#	./retry.sh > "$IMAGE.redo"
# or
#	./retry.sh 512 > "$IMAGE.redo"
# or
#	./retry.sh 512 drive > drive.redo

OOPS()
{
echo "OOPS: $*" >&2
exit 23
}

IMG="${1:-$IMAGE}"

while read -ru6 redo off len
do
	case "$redo" in
	redo)	;;
	*)	OOPS "redo is $redo";;
	esac

	echo "do $off $len" &&
	if
		./redo.py $off $len ||
		./redo.py $off $len ||
		./redo.py $off $len
		
	then
		echo "ok $off $len"
	else
		echo "ko $off $len"
		echo "err $off $len" >> "$IMG.redo.log"
	fi
done 6<"$IMG.redo"

