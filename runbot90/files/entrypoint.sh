#!/bin/bash
set -e

# Change owner all volumes to avoid conflicts with uid
chown -R runbot:runbot /home/runbot
chown root:root -R /var/lib/docker
chown root:root -R /var/log/supervisor
chmod ugo+rwx /tmp

# Set psql environment variables
source /home/runbot/.db_source

# Start supervisor with all daemon
/usr/bin/supervisord

