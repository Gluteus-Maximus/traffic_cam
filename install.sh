#!/bin/bash
# Recommend run as normal user to allow unprivileged use
# Run from same directory as program file
PROG_FILE=$(pwd)/traffic-cam
CONF_FILE=$(pwd)/.traffic-cam.conf
ERR_FILE=/var/log/test_traffic-cam.log
PATH_FILE=/etc/profile.d/traffic-cam.sh

#TODO: echo messages
echo "Create config file:    '$CONF_FILE'"
touch $CONF_FILE
chmod 664 $CONF_FILE
echo "   done"
### Sudo Commands ###
echo "Create error file:     '$ERR_FILE'"
sudo touch $ERR_FILE
sudo chmod 664 $ERR_FILE
echo "   done"
# Add global PATH update to /etc/profile.d/
echo "Add program to PATH:   '$PATH_FILE'"
# Source profile.d?? How??
echo "   done"
echo "Pre-configure program: '$PROG_FILE'"
# sudo chown root traffic-cam
# sudo chgrp root traffic-cam
# sudo chmod +x traffic-cam ##Specify permissions 755
echo "   done"
