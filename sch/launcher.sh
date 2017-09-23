#!/bin/bash
###################################################
# Script for launching the server.
#
# Launch from inside the appointment_scheduler dir
###################################################

# Launch the server in the background and disown it from this terminal
# session.
export FLASK_APP=itsjustflaskr.py
flask run
#flask run > server.log &
#disown