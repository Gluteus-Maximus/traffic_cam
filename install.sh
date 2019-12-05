#!/usr/bin/bash
# Recommend run as normal user to allow unprivileged use
PROG_FILE=traffic-cam
CONF_FILE=.traffic-cam.conf
ERR_FILE=/var/log/traffic-cam.log

#TODO: echo messages
touch $CONF_FILE
chmod 666 $CONF_FILE
touch $ERR_FILE
chmod 666 $ERR_FILE
### Sudo Commands ###
# Add global PATH update to /etc/profile.d/
# Source profile.d?? How??
# Get root credentials
# sudo chown root traffic-cam
# sudo chgrp root traffic-cam
# sudo chmod +x traffic-cam ##Specify permissions 755
