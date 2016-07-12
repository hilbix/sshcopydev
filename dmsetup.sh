#!/bin/bash

OOPS()
{
echo "OOPS: $*" >&2
exit 23
}

numeric()
{
case "$1" in
''|*[^0-9]*)    OOPS "numeric? $1";;
esac
}

x() { "$@"; }
o() { x "$@" || OOPS "ret $?:" "$@"; }
s() { eval "$1="'"$("${@:2}")"' || OOPS "ret $?:" "$1" "=" "${@:2}"; }

last=()
: put offset end setting
put()
{
if	[ -n "$1" ]
then
	[ ".$1" = ".$2" ] && return
	[ "$1" -lt "$2" ] || OOPS "$1 > $2"
	if [ ".${last[*]}" = ".${*:3}" ] && [ ".$1" = ".$lend" ]
	then
		lend="$2"
		return
	fi
fi

if [ -n "${last[*]}" ]
then
	printf '%-10d %-10d' "$lstart" "$[$lend-$lstart]"
	printf ' %q' "${last[@]}"
	printf '\n'
	[ -z "$1" ] || [ ".$lend" = ".$1" ] || OOPS "gap: $lend $1"
fi
last=("${@:3}")
lstart="$1"
lend="$2"
}

DRIVE="${1:-brokendrive}"

s FILE readlink -e "$IMAGE.img"
s LOOP losetup -f
s SIZE stat --printf=%s "$FILE"

let blocks=SIZE/512

cat <<EOF
losetup -D
sleep 1
dmsetup remove '$DRIVE'
sleep 1
losetup -D
rmmod loop
sleep 1
! grep ^loop /proc/modules &&
modprobe loop max_part=16 &&
losetup -a
losetup $LOOP "$IMAGE.img" &&
dmsetup create '$DRIVE' << EOF &&
EOF

BLK=512
pos=0
while read -ru6 error offset length
do
	case "$error" in
	err)    ;;
	*)      OOPS "Wrong line: $error $offset $length";;
	esac
	numeric "$offset"
	numeric "$length"

	let o=offset/BLK
	let l=length/BLK

	[ $[o*BLK] = $offset ] || OOPS "$offset not $BLK aligned"
	[ $[l*BLK] = $length ] || OOPS "$length not $BLK aligned"

	[ "$pos" -le "$o" ] || OOPS "Rewind?  $pos > $o"

	put $pos $o	linear $LOOP $pos
	let pos=o+l
	put $o   $pos	error

done 6<"${1:-$IMAGE.log}"

put $pos $blocks	linear $LOOP $pos
put

echo EOF

cat <<EOF

losetup -a &&
sleep 1 &&
losetup --partscan -f '/dev/mapper/$DRIVE'

echo ------------

losetup -a

ls -la /dev/loop?p*
EOF

losetup -a >&2

