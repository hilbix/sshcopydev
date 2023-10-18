#!/usr/bin/env python3
#
# Just test connection

TIMEOUT_CONN = 10
TIMEOUT_READ = 45

print('HW')

import os
import sys
import paramiko

try:
	HOST    = os.environ['HOST']
	KEY     = os.environ['KEYFILE']
	FETCH1  = os.environ['FETCH1']
	FETCH2  = os.environ['FETCH2']
	DEV1    = os.environ['DEV1']
	DEV2    = os.environ['DEV2']
except:
	print("Please source SETTINGS first")
	sys.exit(1)

#bs  = paramiko.SFTPFile.MAX_REQUEST_SIZE

print('ONE')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

print('TWO')

ssh.connect(HOST, username='root', look_for_keys=False, key_filename=KEY, timeout=TIMEOUT_CONN)

print('THREE')

ftp = ssh.open_sftp()
ftp.get_channel().settimeout(TIMEOUT_READ)

print('FOUR')

dev = ftp.open(DEV1, mode='rb', bufsize=0)
dev.settimeout(TIMEOUT_READ)
dev.close()

print('FIVE')

ftp.close()
ssh.close()

print('SIX')
