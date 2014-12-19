#!/usr/bin/python

from os import listdir, stat, chown, path
from subprocess import Popen, call
from shutil import copy2
import pwd

filestore_path = '/home/runbot/instance/odoo/openerp/filestore'
configfile_path = '/home/runbot/instance/config/odoo.conf'

st = stat(filestore_path)
owner = pwd.getpwuid(st.st_uid).pw_name
if owner != "runbot":
    call(["chown", "-R", "runbot", filestore_path])

if not path.isfile(configfile_path):
    copy2("/external_files/odoo.conf", configfile_path)

st = stat(configfile_path)
owner = pwd.getpwuid(st.st_uid).pw_name
if owner != "runbot":
    call(["chown", "-R", "runbot", configfile_path])

call(["/usr/bin/supervisord"])
