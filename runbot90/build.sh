#!/bin/bash

cp ${HOME}/.ssh/id_rsa "$(dirname $0)/files/id_rsa"
# docker build -t runbot:90 $1 "$(dirname $0)"
ansible/start.sh
