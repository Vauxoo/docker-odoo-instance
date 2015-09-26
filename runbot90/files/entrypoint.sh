#!/bin/bash

set -e

# chown -R runbot:runbot ${EXTRA_ADDONS}/odoo-extra/runbot/static
# chown -R runbot:runbot /home/runbot/.local/share/Odoo/filestore
# chown -R runbot:runbot /var/log/supervisor
# chown -R runbot:runbot /var/lib/docker
chown -R runbot:runbot /home/runbot
chmod ugo+rwx /tmp

source /home/runbot/.db_source
/usr/bin/supervisord
