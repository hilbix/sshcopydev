# SSH copy dev

Copy a device using SSH (SFTP)

> Warning!  THIS IS PRE-ALPHA PRERELEASE quality and nealry UNTESTED.  It is far from being perfect.
> It is far from being usable for people who do not understand the code presented here.  It also was done in a hurry.  Sorry.
>
> I just hacked this together for me because I had some trouble to solve at my side.
> And then I hacked it such, that it might be helpful to others.
>
> This is only published for others to be meant to be helpful in case they need a method like this to just copy a device in a situation, where you only have an ssh connection and barely nothing more.

- This only needs `sftp` access to the remote machine using `ssh` key-files.
- So all you need prepare is, that you can do `sftp root@broken.host` without any password prompt
- Then you can copy a device (which possibly contains errors)
- If the network connection breaks the `copy` stops, puts you into a shell, which you then exit if.
- If the remote machine crashes (it is broken, right?) you can reboot it into rescue again and continue.
- Note that the local machine (where you run this) needs to to be rock solid stable.  If not, choose something different.
- Note that the remote device must not be altered during this process.  However it can be accessed with different names, just in case.
  - For example, I had a Linux machine which became so instable, that it often only booted in a very tiny (BSD) rescue which only offered ssh access and nearly no Linux specific tools.
  - Because of this this method allows 2 different device names, such that you can switch between 2 sets of rescue while the copy runs.  Just edit SETTINGS accordingly before(!) starting the `copy`.

## How to use

Assumptions:

- `HOST` is the broken system
- You know the device which needs to be recovered, and the device name is unique (it may have more than one name in case you boot different systems, but both names must be unique)
- `sftp root@HOST` works, so `ssh` is set up properly
- `python` with `python-paramiko` is available locally (`apt-get install python python-paramiko`)
- Current directory has a lot of space to take up all the image of the remote drive you want to copy
- Your local system probably is Linux (sorry, no solution for Windows)
- Network connection is somewhat stable, so interrupts can always happen
- Remote machine is somewhat stable, so it may break down now and then
- Remote device is not changed while you try to recover it, even if you reboot the remote machine
- You are using `/bin/bash` as your shell (else perhaps some things might not work)


```
git clone https://github.com/hilbix/sshcopydev.git
cd sshcopydev
vim SETTINGS
. ./SETTINGS
touch "$IMAGE.img"
./copy.py
```

- If things break, fix the intermediate problems and restart `./copy.py` until all is copied.
- For safety you need to create the empty image file (see `touch` above) first (so accedentally running `copy.py` does no harm). 

Then examine `$IMAGE.log`.  If there are no errors listed it is likely you are ready.

Else retry the failed sectors.  Note that the failures might have come from network outages, not neccessarily from defective sectors:

```
./retry.sh > "$IMAGE.redo"
./redo.sh
```

- This creates an "$IMAGE.redo.log"
- Now `mv -f "$IMAGE.redo.log" "$IMAGE.log"` and you can start another `retry.sh`+`redo.sh` cycle if you like, until you are happy.

