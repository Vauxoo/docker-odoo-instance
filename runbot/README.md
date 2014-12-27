Odoo Runbot
===========

This docker image is for Odoo runbot hacked by Vauxoo.

To run this image you must install docker[1] then pull Odoo runbot docker image from::

    docker pull vauxoodeveloper/docker-odoo-instance

After the download process is completed you can run the container with::

    docker run -e "DB_HOST=your_db_host" -v path_to_sshkeys:/home/runbot/.ssh -t runbot

Where:

*path_to_sshkeys*: path to ssh keys that will be used for connecting to github, bitbucket and so
*your_db_host*: database server hostname or ip

*NOTE:* when you mount the volume be sure you have hithub, bitbucker, launchpad and gitlab in the known hosts file

You can add additional env vars to configure Odoo instance::

    docker run -e "DB_HOST=your_db_host" -e "DB_USER=the_user" -e "DB_PASSWORD=the_user_password" -e "ADMIN_PASSWD=the_admin_pass" -v path_to_sshkeys:/home/runbot/.ssh -t runbot

And any other parameter defined in the Odoo config file, you must type it in uppercase if you want the entry point detect it.