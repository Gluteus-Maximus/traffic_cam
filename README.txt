Note: If traffic_cam directory is moved or files renamed after creating cron
job ("./traffic_cam config --apply") auto-logging functionality will break.

Note: Error log will go in "/var/log/traffic_cam.log". Access is restricted
    to root.

Note: traffic_cam.py write permissions should be limited to root.
    Recommended permissions are "rwxr-xr-x root root". This is to limit
    potential security vulnerabilities which would be created if normal
    users could alter the executable.

Note: Logfile (default netdev.log) will be created by root if not
created before.  If read access is needed for other users there are several
options:
    > "$ touch netdev.log" in directory as traffic_cam.py before running
    > "$ sudo chmod +r netdev.log"
    > "$ sudo chown <username> netdev.log"

Note: Cronjob is stored in "/etc/cron.d/traffic_cam_cron". This is only
    accessible by root and jobs within this file must be run as root
    (specified in the cron string). This file is intended to be modified
    or deleted through "./traffic_cam.py config" mode.

Note: "./traffic_cam.py config" mode must be run as root. This is to limit
    potential security vulnerabilities which could be created if normal
    users could alter the cronjob or config file.
    "$ sudo ./traffic_cam.py config ..."

Note: In "./traffic_cam.py history" modes values for "--timeslice" or
    "--time X Y" can be provided for different effects:
    > ... --time X Y   : from epoch timestamp X to Y
    > ... --time 0 0   : from earliest log to latest
    > ... --time -X -Y : from X minutes ago to Y minutes ago

Note: "./traffic_cam.py history --logfiles ..."
    Specify Input NetDev Logfile(s) (if different from filepath in config).

Note: .traffic_cam.conf must have read permissions for all users of
    program.

Note: Add traffic_cam to PATH ##TODO: make bash setup script

Note: To install, move file directory to desired location, then run
install.sh as a normal user (you will need sudo credentials for part of
this script).
