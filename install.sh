#!/bin/bash
# Recommend run as normal user to allow unprivileged use of certain files
# Run from same directory as program file
PROG_FILE=$(pwd)/traffic-cam
CONF_FILE=$(pwd)/.traffic-cam.conf
ERR_FILE=/var/log/traffic-cam.log
PATH_FILE=/etc/profile.d/traffic-cam.sh

#TODO: check results before 'done'
echo "Create config file:  '$CONF_FILE'"
touch $CONF_FILE
chmod 664 $CONF_FILE
echo "   done"
### Sudo Commands ###
echo "Create error file:   '$ERR_FILE'"
sudo touch $ERR_FILE
sudo chmod 664 $ERR_FILE
echo "   done"
# Add global PATH update to /etc/profile.d/
echo "Add program to PATH: '$PATH_FILE'"
sudo touch $PATH_FILE
# echo file contents to PATH_FILE
CONTENT="#!/bin/bash"
CONTENT+="\n# Add traffic-cam directory to PATH"
CONTENT+="\n"
CONTENT+="\nPATH=$PATH:$(pwd)"
echo $CONTENT
sudo sh -c "echo $CONTENT > $PATH_FILE"
# Source profile.d?? How??
echo "   done"
echo "Configure program:   '$PROG_FILE'"
sudo chown root $PROG_FILE
sudo chgrp root $PROG_FILE
sudo chmod 755 $PROG_FILE # all users: read/exe, only root: write
echo "   done"
