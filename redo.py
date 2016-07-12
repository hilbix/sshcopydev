#!/usr/bin/env python
#
# Called from redo.sh

PREFETCH  = 0x100000
TIMEOUT_CONN = 10
TIMEOUT_READ = 45

import os
import sys
import time
import socket
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(os.environ['HOST'], username='root', compress=False, timeout=TIMEOUT_CONN)

ftp = ssh.open_sftp()
ftp.get_channel().settimeout(TIMEOUT_READ)

try:
	dev = ftp.open(os.environ['DEV1'], mode='rb', bufsize=0)
except IOError:
	dev = ftp.open(os.environ['DEV2'], mode='rb', bufsize=0)

dev.settimeout(TIMEOUT_READ)
	

off = int(sys.argv[1])
cnt = int(sys.argv[2])

dev.seek(off)
try:
	dat = dev.read(cnt)
except IOError as e:
	print repr(e)
	sys.exit(1)

out = open(os.environ['IMAGE'+'.img', 'rb+')
out.seek(off)
out.write(dat)

