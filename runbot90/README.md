
============================
Runbot 90 with travis2docker
============================

This docker was written for run a container of runbot with all configurated
to work directly with `runbot_travis2docker module`

Installation
============

To install this container, you need to:
 
 * Go to runbot90 folder and install `requirements.txt` file execute: 
  * `# pip install requirements.txt`
 * Remove password to your ssh private key.
  * Follow next [instructions](http://www.thinkplexx.com/learn/howto/security/ssl/remove-passphrase-password-from-private-rsa-key)
 * Add permission to run `docker` command to your user.
  
Usage
=====

To use this container, you need to:

* Go to runbot90/ansible folder and execute `start.sh` script
 * `$: ./start.sh`
  * Wait too much time to finish (download large images, build, run...)
* Now you have 2 container
 * postgres
 * runbot
   * runbot container has a link to postgres container.
* Attach to runbot container
 * `$: docker exec -it runbot90 bash`
* (into container) Restart odoo server executing
  * `# supervisorctl stop odoo`
  * `#: su runbot`
  * `$: source /home/runbot/.db_source`
  * `$: /home/runbot/instance/odoo/odoo.py --config=/home/runbot/instance/config/odoo_runbot.conf`
* (out of container, in main computer) Connect to odoo instance
  * Get port published of runbot docker
    * `$ docker port runbot_90 | grep 8069`
      * ouput of example: `8069/tcp -> 0.0.0.0:33177`
  * Open browser:
    * `http://127.0.0.1:33177`
    * Note: If you use boot2docker, remote docker server or docker-machine you will need get the ip and publish the port from firewall or you can use ngrok too.
