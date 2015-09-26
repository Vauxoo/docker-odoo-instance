#!/bin/bash

ansible-playbook "$(dirname $0)/start_runbot.yml" -c local -i "$(dirname $0)/inventory"
