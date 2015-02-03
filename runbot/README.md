Odoo Runbot
===========

## Executing directly with docker

This docker image is for Odoo runbot hacked by Vauxoo.

To run this image you must install docker[1] then pull Odoo runbot docker image from::

    docker pull vauxoodeveloper/docker-odoo-instance

After the download process is completed you can run the container with::

    docker run -e "DB_HOST=your_db_host" -h hostname -v path_to_sshkeys:/home/runbot/.ssh -t runbot

Where:

*path_to_sshkeys*: path to ssh keys that will be used for connecting to github, bitbucket and so
*your_db_host*: database server hostname or ip
*hostname*: is a mandatory parameter that specify the hostname where you will use to connect ie (runbot.vauxoo.com)

*NOTE:* when you mount the volume be sure you have hithub, bitbucker, launchpad and gitlab in the known hosts file

You can add additional env vars to configure Odoo instance::

    docker run -e "DB_HOST=your_db_host" -e "DB_USER=the_user" -e "DB_PASSWORD=the_user_password" -e "ADMIN_PASSWD=the_admin_pass" -v path_to_sshkeys:/home/runbot/.ssh -h hostname -t runbot

And any other parameter defined in the Odoo config file, you must type it in uppercase if you want the entry point detect it.

## Executing using ansible files

*NOTE:* In order to use ansible files you must install ansible (http://docs.ansible.com/intro_installation.html#latest-releases-via-pip)

First you must copy to the host where you want to install the runbot image, then you can execute it as follows::

	ansible-playbook start_runbot.yml -c local -i inventory

Optionally change the defaults parameters edit *vars.yml* file, there you can change hostname, mapped ports, db server configuration, etc.

Most of the default env vars can be changed by editing the *vars.yml* file but if you want to add additionar env vars or edit the existing ones find the following line in the *start_runbot.yml* file:

	env: "DB_HOST={{ db_server }},DBFILTER={{ db_filter }},DB_NAME={{ db_name }},WITHOUT_DEMO=False,ODOO_CONFIG_FILE={{ odoo_config_file }}"

And change as you need.

