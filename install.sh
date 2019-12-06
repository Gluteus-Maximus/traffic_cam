#!/bin/bash
# Recommend run as normal user to allow unprivileged use of certain files
# Run from same directory as program file
PROG_FILE=$(pwd)/traffic-cam
CONF_FILE=$(pwd)/.traffic-cam.conf
ERR_FILE=/var/log/traffic-cam.log
SYM_LINK=/usr/local/bin/traffic-cam  # cli command defined by name of sym link
#PATH_FILE=/etc/profile.d/traffic-cam.sh

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

'''
# Add global PATH update to /etc/profile.d/
echo "Add program to PATH: '$PATH_FILE'"
#sudo touch $PATH_FILE
# echo file contents to PATH_FILE
CONTENT="#!/bin/bash"
CONTENT+="\n# Add traffic-cam directory to PATH"
CONTENT+="\n"
CONTENT+="\nPATH=\$PATH:$(pwd)"
sudo sh -c "echo '$CONTENT' > $PATH_FILE"
source $PATH_FILE  #TODO: source not working
echo "   done"
'''
# Add Symbolic Link
sudo ln -s $PROG_FILE $SYM_LINK

# Pre-Configure Program File (permissions)
echo "Configure program:   '$PROG_FILE'"
sudo chown root $PROG_FILE
sudo chgrp root $PROG_FILE
sudo chmod 755 $PROG_FILE # all users: read/exe, only root: write
echo "   done"
