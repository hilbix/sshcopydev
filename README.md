# SSH copy dev

Copy a device using SSH (SFTP)

> Warning!  THIS IS PRE-ALPHA PRERELEASE quality and nealry UNTESTED.  It is far from being perfect.
> It is far from being usable for people who do not understand the code presented here.  It also was done in a hurry.  Sorry.
>
> I just hacked this together for me because I had some trouble to solve at my side.
> And then I hacked it such, that it might be helpful to others.
>
> This is only published for others to be meant to be helpful in case they need a method like this to just copy a device in a situation, where you only have an ssh connection and barely nothing more.

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

T.B.D. (Sorry, no time to explain the next steps.  Use the source.)
