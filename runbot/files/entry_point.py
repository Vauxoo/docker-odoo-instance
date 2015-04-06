#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Entry point for Dockerized aplications, this works mainly with
Odoo instances that will be launched using supervisor
'''
from os import stat, path, getenv, listdir, remove
from subprocess import call
from shutil import copy2, rmtree
import pwd
import fileinput
import redis
import logging
import sys
import traceback
import psycopg2
import ConfigParser


logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s:[%(asctime)s] - %(name)s.%(module)s - %(message)s')
logger = logging.getLogger("entry_point")

USER_NAME = getenv('ODOO_USER') and getenv('ODOO_USER') or 'odoo'
FILESTORE_PATH = getenv('ODOO_FILESTORE_PATH') \
    and getenv('ODOO_FILESTORE_PATH') \
    or '/home/%s/.local/share/Odoo/filestore' % USER_NAME
CONFIGFILE_PATH = getenv('ODOO_CONFIG_FILE') \
    and getenv('ODOO_CONFIG_FILE') \
    or '/home/%s/.openerp_serverrc' % USER_NAME


def change_values(file_name, getter_func):
    '''
    Changes value from a config file, new values are gotten
    from redis server or env vars

    :param str file_name: Config file name
    :getter_func: Fucnttion that will be used for getting new values
    '''
    for line in fileinput.input(file_name, inplace=True):
        new_str = line
        logger.debug("Line readed: %s", line.strip())
        parts = line.split("=")
        logger.debug("Parts: %s", len(parts))
        if len(parts) > 1:
            search_str = parts[0].upper().strip()
            value = getter_func(search_str)
            logger.debug("Search for: %s and value is: %s", search_str, value)
            if value:
                new_str = "%s = %s" % (parts[0], value)
        print(new_str.replace('\n', ''))


def get_owner(file_name):
    '''
    This function gets owner name from system for a directory or file

    :param str file_name: File or directory name
    :returns: Owner name
    '''
    file_stat = stat(file_name)
    try:
        owner = pwd.getpwuid(file_stat.st_uid).pw_name
    except KeyError:
        owner = "None"
    logger.debug("Owner of %s is %s", file_name, owner)
    return owner


def get_redis_vars(var_name):
    '''
    This function gets values from a has stored in redis

    :param str var_name: The key or var name
    :returns: Value
    '''
    res = None
    r_server = redis.Redis(getenv('REDIS_SERVER'))
    if getenv('CLIENT_NAME'):
        key = '%s_%s' % (getenv('CLIENT_NAME'), getenv('STAGE'))
    else:
        key = getenv('STAGE')

    try:
        res = r_server.hget(key, var_name)
    except redis.exceptions.ConnectionError as res_error:
        logger.exception("Error trying to read from redis server: %s",
                         res_error)
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
    return res


def delete_build_wo_logs(builds_path):
    ''' Delete static build files

    :param str builds_path: The path to static build files
    '''
    if path.exists(builds_path):
        for build_path in listdir(builds_path):
            if path.isdir(build_path):
                for item in listdir(build_path):
                    path_item = path.join(build_path, item)
                    if path.isdir(path_item):
                        if item != 'logs':
                            rmtree(path_item)
                        elif path.isfile(path_item):
                            remove(path_item)


def run_sql(sql, db_config):
    ''' Runs a SQL statement in the specified database

        The dict db_config is espected to have the following elements:
        {
            db_name: Database name
            db_user: User to use to connect to the database
            db_pass: Password to use for the connection
            db_host: Db host name or ip (default to docker ip interface)
            db_port: Db port number (default to 5432)
        }
    :param dict db_config: Database connection parameters
    :returns: the query result
    '''
    str_conn = 'dbname=%s user=%s host=%s port=%s' % \
               (db_config.get('db_name'), db_config.get('db_user'),
                db_config.get('db_host'), db_config.get('db_port'))
    logger.debug('Connection sting: %s', str_conn)
    if db_config.get('db_pass'):
        str_conn = '%s password=%s' % (str_conn, db_config.get('db_pass'))

    logger.info('Trying to connect to the PostgreSQL server')
    try:
        conn = psycopg2.connect(str_conn)
        conn.set_isolation_level(0)
    except Exception as e:
        logger.exception('Could not connect to the database: %s', e.message)
        raise

    cur = conn.cursor()
    res = None
    try:
        logger.debug('Query: %s', sql)
        cur.execute(sql)
    except Exception as e:
        logger.exception('Could not excecute the query: %s', e.message)
        raise
    else:
        if cur.rowcount == -1 or sql.strip().upper().startswith('INSERT') or \
           sql.strip().upper().startswith('UPDATE'):
            res = True
        else:
            res = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    return res


def clean_runbotbds(db_config):
    ''' This method clean an existing runbot database:
            1 - Drops builds databases
            2 - Update builds state and set them to done
            3 - Kill connections older than 10 minutes

        The dict db_config is espected to have the following elements:
        {
            db_name: Database name
            db_user: User to use to connect to the database
            db_pass: Password to use for the connection
            db_host: Db host name or ip (default to docker ip interface)
            db_port: Db port number (default to 5432)
        }
    :param dict db_config: Database connection parameters
    '''
    drop_dbs = "SELECT datname FROM pg_catalog.pg_database d " + \
               "WHERE pg_catalog.pg_get_userbyid(d.datdba) = '%s' " % \
               db_config.get('db_user')
    drop_dbs = drop_dbs + \
        "AND (datname like '%-base' OR datname like '%-all')"
    update_state = "UPDATE runbot_build SET state='done'"
    kill_connections = "select datid, state_change, now()-state_change " + \
                       "AS ago, pg_terminate_backend(pid) " + \
                       "FROM pg_stat_activity " + \
                       "WHERE now()-state_change >= INTERVAL '10 minutes' " + \
                       "ORDER BY state_change ASC;"

    logger.info('Drop databases')
    dbs = run_sql(drop_dbs, db_config)
    if dbs:
        for db in dbs:
            logger.debug('Drop db %s', db[0])
            run_sql('DROP DATABASE "%s"' % db[0], db_config)

    logger.info('Update state')
    run_sql(update_state, db_config)

    logger.info('Kill connections')
    run_sql(kill_connections, db_config)


def read_db_config(config_file):
    ''' Reads the db config from Odoo config file to use it in case
    in necesary to clean the runbot database

    :param str config_file: Full name and path to the config file

    :returns: A dict with the configuration
    '''
    config = ConfigParser.RawConfigParser()
    config.read(config_file)
    db_config = {}
    db_config.update({'db_host': config.get('options', 'db_host')})
    db_config.update({'db_port': config.get('options', 'db_port')})
    db_config.update({'db_user': config.get('options', 'db_user')})
    db_config.update({'db_pass': config.get('options', 'db_password')})
    db_config.update({'db_name': config.get('options', 'db_name')})
    return db_config


def main():
    '''
    Main entry point function
    '''
    logger.info("Entering entry point main function")
    if not path.isfile(CONFIGFILE_PATH):
        copy2("/external_files/odoo_runbot.conf", CONFIGFILE_PATH)

    if getenv('REDIS_SERVER'):
        getter_func = get_redis_vars
        logger.info("Using redis server: %s", getenv('REDIS_SERVER'))
    else:
        getter_func = getenv
        logger.info("Using env vars")

    change_values(CONFIGFILE_PATH, getter_func)
    bd_config = read_db_config(CONFIGFILE_PATH)
    clean_runbotbds(bd_config)
    delete_build_wo_logs(
        '/home/%s/instance/extra_addons/odoo-extra/runbot/static/build'
        % USER_NAME)
    if not path.isfile(FILESTORE_PATH):
        call(["mkdir", "-p", FILESTORE_PATH])

    call(["chown", "-R", "%s:%s" % (USER_NAME, USER_NAME), "/home/%s"
          % USER_NAME])
    call(["chmod", "ugo+rwx", "/tmp"])
    logger.info("All changes made, now will run supervidord")
    call(["/usr/bin/supervisord"])


if __name__ == '__main__':
    main()
