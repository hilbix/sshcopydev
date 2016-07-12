# SSH copy dev

Copy a device using SSH (SFTP) from a broken machine

> Warning!
>
> This was put together in a hurry from some obsure scripts I once created for myself only.
> It was changed on-the-fly without being tested afterwars, such that you can probably use it.
> It may contain bugs.  So please do not blame me when you find errors or it kills something on your side!
> This is not meant only to be an example how it can be done, so please use it wisely.
>
> Note that documentation might be wrong, as it, also, was done in a hurry.
> If you find any problems, you can open an issue or better, create an update and send me pull-requests.
>
> Thank you very much!
>
> THIS IS PRE-ALPHA PRERELEASE quality and nealry UNTESTED.  It is far from being perfect.  Use at your own risk!  Use with care!
> This is only published for others to be meant to be helpful in case they need it.

- This only needs `sftp` access to the remote machine using `ssh` key-files.
- So all you need prepare is, that you can do `sftp root@broken.host` without any password prompt
- Then you can copy a device (which possibly contains errors)
- If the network connection breaks the `copy` stops, puts you into a shell, which you then exit if.
- If the remote machine crashes (it is broken, right?) you can reboot it into rescue again and continue.
- Note that the local machine (where you run this) needs to to be rock solid stable.  If not, choose something different.
- Note that the remote device must not be altered during this process.  However it can be accessed with different names, just in case.
  - For example, I had a Linux machine which became so instable, that it often only booted in a very tiny (BSD) rescue which only offered ssh access and nearly no Linux specific tools.
  - Because of this this method allows 2 different device names, such that you can switch between 2 sets of rescue while the copy runs.  Just edit SETTINGS accordingly before(!) starting the `copy`.

Other things to mention:

- `ddrescue` is a far better way to copy a broken device.
- However in case the broken drive is in a broken machine and all you have is a network connection there, `ddrescue` cannot be used, because you cannot run it on the broken machine.
- Sadly `sshfs` is not capable to forward remote devices (*you will see you local devices instead!*), so you cannot run it on a local machine either.
- Hence I needed a way to access a remote `/dev/` file somehow.  This here is the result.


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
mv -f --backup=t "$IMAGE.redo.log" "$IMAGE.log"
```

- `redo.sh` creates an "$IMAGE.redo.log"
- You can start another `retry.sh`+`redo.sh` cycle if you like, until you are happy.
- In the last cycle(s) use `./retry.sh 512 > "$IMAGE.redo"` when your drive has 512 byte sectors and you want to pull the last bits from it.

Afterwards you can simulate your defective drive, including the read errors!.  There is a helper to properly setup `dmsetup` which is called `dmsetup.sh`

Call it like this:

```
./dmsetup.sh name-you-want
```

If you leave away the `name-you-want` it is called `brokendrive`.

This step does not do anything.  It just prints out the neccessary commands you need to do to `stdout`.  If you are happy with this you can do (as `root`):

```
./dmsetup.sh name-you-want | bash
```

Do not forget to source `. SETTINGS` if you switched to root using `sudo` or similar.

> Note about Ubunut:
> 
> Ubuntu has `loop` compiled in the kernel.  Hence you cannot change parameters of the loop devices while running.  This is very sad and very bad.
> To change the loop devices properly (partitions!) you need a kernel boot parameter like `loop.max_part=16` in `GRUB_CMDLINE_LINUX_DEFAULT` in file `/etc/default/grub`
> (then `update-grub` and `reboot`).

