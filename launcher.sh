#!/bin/bash
###################################################
# Script for launching the webserver.
#
# Launch using:
# 	sudo -s
# 	source launcher.sh
#
# Launch from inside the root 'website' directory
###################################################

# Launch the server in the background and disown it from this terminal
# session.
python webserver.py flaskapp:app > ~/server.log &
disown

# Check that the server is running
echo "Check successful launch using 'sudo fuser 80/tcp'"
