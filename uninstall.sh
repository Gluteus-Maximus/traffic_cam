#!/bin/bash
# Remove traffic-cam artifacts from filesystem
ERR_FILE=/var/log/traffic-cam.log
SYM_LINK=/usr/local/bin/traffic-cam
CRON_FILE=/etc/cron.d/traffic-cam-cron

sudo rm $ERR_FILE
sudo rm $SYM_LINK
sudo rm $CRON_FILE
