#!/bin/bash
#
# This is called when a failure is detected (connection problem)
# Most often this means, the remote machine has crashed or a network outage
#
# Try to resolve things automatically, if you are not able to do so, drop in a shell

# Check if machine available, then just retry
ssh -o BatchMode=yes -o KbdInteractiveAuthentication=no -o PasswordAuthentication=no -o StrictHostKeyChecking=no -o ConnectTimeout=10 -o ServerAliveInterval=1 -o ServerAliveCountMax=3 "root@$HOST" true && exit

# Reset the remote mache with some obsuce procedure
robot/rescue.sh && exit

# Nope, enter shell, leave it to the admin
echo
echo "### Copy interrupted.  Please fix problem, then exit this shell"
echo
date
exec bash
