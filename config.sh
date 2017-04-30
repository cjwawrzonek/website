#!/bin/bash
# Simple configuration script for webserver VM's
# [config.sh] 

LOG_DIR=/var/log
ROOT_UID=0     # Only users with $UID 0 have root privileges.
E_NOTROOT=87   # Non-root exit error.

# Run as root, of course.
if [ "$UID" -ne "$ROOT_UID" ]
then
  echo "Must be root to run this script."
  exit $E_NOTROOT
fi  

# Python configuration commands
easy_install pip
pip install virtualenv
pip install flask

# success
exit 0