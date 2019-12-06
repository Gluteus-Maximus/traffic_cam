#!/bin/bash
# This script is idempotent, and can be run at any time to update file
#  location, recreate deleted error or config file, or fix program file
#  permissions.
# Recommend run as normal user to allow unprivileged use of certain files
# Run from same directory as program file
PROG_FILE=$(pwd)/traffic-cam
CONF_FILE=$(pwd)/.traffic-cam.conf
ERR_FILE=/var/log/traffic-cam.log
SYM_LINK=/usr/local/bin/traffic-cam  # cli command defined by name of sym link
#TODO: ^ if /usr/local/bin/ exists, else /usr/bin/

#TODO: check results before 'done'
# Add Config File
echo "Create config file:  '$CONF_FILE'"
touch $CONF_FILE
chmod 664 $CONF_FILE
echo "   done"

# Add Error Log
echo "Create error file:   '$ERR_FILE'"
sudo touch $ERR_FILE
sudo chmod 664 $ERR_FILE
echo "   done"

# Add Symbolic Link (global cli calls)
sudo ln -sf $PROG_FILE $SYM_LINK

# Pre-Configure Program File (permissions)
echo "Configure program:   '$PROG_FILE'"
sudo chown root $PROG_FILE
sudo chgrp root $PROG_FILE
sudo chmod 755 $PROG_FILE # all users: read/exe, only root: write
echo "   done"
