#!/usr/bin/env python3

PREFETCH  = 0x100000
TIMEOUT_CONN = 10
TIMEOUT_READ = 45

import os
import sys
import time
import socket
import paramiko

#print("NOPE"); os.exit(-1)


# Variables, see file SETTINGS
try:
	HOST    = os.environ['HOST']
	KEY     = os.environ['KEYFILE']	# be sure it starts with "-----BEGIN RSA PRIVATE KEY-----" not "OPENSSH"!
	FETCH1  = os.environ['FETCH1']
	FETCH2  = os.environ['FETCH2']
	DEV1    = os.environ['DEV1']
	DEV2    = os.environ['DEV2']
	IMAGE   = os.environ['IMAGE']
except:
	print("Please source SETTINGS first")
	sys.exit(1)

bs  = paramiko.SFTPFile.MAX_REQUEST_SIZE
#PREFETCH  = 0

ssh = None
ftp = None
dev = None

setups = 0
fails = 0
mode = '?'

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def dumpvar(c):
	print('#', repr(c), c.__class__.__module__, c.__class__.__name__)
	print(', '.join("%s:'%s'" % (att, getattr(c,att)) for att in dir(c) if not callable(getattr(c,att)) and not att.startswith('__')))

def note(c):
	sys.stdout.write(c)
	sys.stdout.flush()

def teardown():
	global dev, ftp, ssh, mode

	try:
		dev.close()
	except:
		pass
	dev = None
	try:
		ftp.close()
	except:
		pass
	ftp = None

	try:
		ssh.close()
	except:
		pass

	mode = 'C'


def setup():
	global fails, ftp, dev, setups, mode, HOST, DEV1, DEV2

	try:
		note('c')
		ssh.connect(HOST, username='root', compress=True, look_for_keys=False, key_filename=KEY, timeout=TIMEOUT_CONN)

		note('f')
		ftp = ssh.open_sftp()
		ftp.get_channel().settimeout(TIMEOUT_READ)

		try:
			note('d')
			dev = ftp.open(DEV1, mode='rb', bufsize=0)
		except IOError:
			note('D')
			dev = ftp.open(DEV2, mode='rb', bufsize=0)

		note('o')
		dev.settimeout(TIMEOUT_READ)
	
		setups += 1
		mode = 'O'

	except:
		fails += 1
		teardown()
		os.system("./fail.sh")
		mode = 'F'


out = open(IMAGE+'.img', 'rb+')
log = open(IMAGE+'.log', 'a')

out.seek(0,2)

off = out.tell()
off &= ~0xfff

print("starting at %5f GB %x" % ( float(off)/0x40000000, off ))

total = 0
speed = 0
num = 1
l=0

start = int(time.time())-1
last = start

errors = 0
cnt = 0
pref = 0
while True:
	cnt += 1
	now = time.time()

	if int(now) != last:
		last = int(now)

		if num>9:
			speed = float(speed * (num-1)) / num
		else:
			num += 1

	delta = now-start
	if delta==0:
		delta = 0.1
	sys.stdout.write('\r%c%s %d:%02d:%02d %dC %dF %dE %14x %fG tot: %fG %fM/s cur: %5fM/s %d %d' % ( "/-\\|"[cnt%4], mode, delta/3600, (delta/60)%60, delta%60, setups, fails, errors, off, float(off)/0x40000000, float(total)/0x40000000, float(total)/delta/0x100000, float(speed)/num/0x100000, pref, l) )
	sys.stdout.flush()

	if mode!='O':
		setup()
		if int(time.time())==now:
			time.sleep(1)
		continue

	try:
		dev.seek(off)
		if not dev._prefetching and pref>0:
			note('p')
			dev.prefetch(off+pref)
		note('r')
		dat = dev.read(bs)

	except (socket.timeout, socket.error, paramiko.ssh_exception.SSHException):
		pref = 0

		# socket.timeout and socket.error are IOError, too
		teardown()
		continue
		
	except IOError as e:
		pref = 0

		errors += 1
		# We have 2 types of IO errors
		# timeout
		# and read errors
		if e.message == 'Failure':
			log.write('err {} {}\n'.format(off,bs))
			log.flush()
			off += bs
			continue

		print("unknown exception:")
		dumpvar(e)
		teardown()
		os.system('bash')
		continue

	note('.')
	if dat=='':
		break

	out.seek(off)
	out.write(dat)

	l = len(dat)

	off += l
	total += l
	speed += l

	pref = PREFETCH
