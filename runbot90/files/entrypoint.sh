#!/bin/bash

set -e

chown -R runbot:runbot /home/runbot
chmod ugo+rwx /tmp

source /home/runbot/.db_source
/usr/bin/supervisord
