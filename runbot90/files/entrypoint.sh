#!/bin/bash
set -e

# Change owner all volumes to avoid conflicts with uid
chown -R runbot:runbot /home/runbot
chown root:root -R /var/lib/docker
chown root:root -R /var/log/supervisor
chmod ugo+rwx /tmp

# Re-add ssh keyscan, support overwrite of -v ssh
ssh-keyscan github.com > /home/runbot/.ssh/known_hosts \
&& ssh-keyscan launchpad.net >> /home/runbot/.ssh/known_hosts \
&& ssh-keyscan bitbucket.org >> /home/runbot/.ssh/known_hosts

# Set psql environment variables
source /home/runbot/.db_source

# Start supervisor with all daemon
/usr/bin/supervisord

