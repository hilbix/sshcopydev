# TODO

Missing things

# Compare

After doing a `./copy.py` you certainly want to do a `./compare.py`, right?

Sorry, I did not came around to do this yet.  There is a very crude compare script, but it is far from usable:

```
#!/bin/bash

DEV="$DEV2"

ok=true

for a in {2..900}
do
	echo -n $'\r'"$a "
	want="$(dd if="$IMAGE.img" bs=10240 count=1024 skip=$[1024*a] 2>/dev/null | md5sum - | awk '{ print $1 }')"
	echo -n $?
	have="$(ssh root@$HOST "dd if="$DEV" bs=10240 count=1024 skip=$[1024*a] 2>/dev/null | md5")"
	echo -n $?
	[ ".$want" = ".$have" ] && continue
	echo
	echo "$a  want $want"
	echo "$a  have $have"
	ok=false
done

$ok
```

