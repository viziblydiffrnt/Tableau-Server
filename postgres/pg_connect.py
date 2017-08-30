import time
import os, sys
from os import path
import more_itertools
from  more_itertools import unique_everseen
from operator import itemgetter
import psycopg2
import sys
import pprint
import requests
import xml.etree.ElementTree as ET
import urllib
import zipfile
import shutil
import yaml
sys.path.append("..")

# import settings from yaml config

with open("config.yml", 'r') as ymlfile:
	cfg = yaml.load(ymlfile)

tab_server_settings = cfg["tab_server_settings"]
postgres_settings = cfg["postgres_settings"]

# Set variables based on Config File
run_mode = tab_server_settings['run_mode']

days_since_viewed = tab_server_settings['days_since_viewed']
days_since_accessed = tab_server_settings['days_since_accessed']

tab_server_pg_db = postgres_settings['tab_server_pg_db']
pg_user = postgres_settings['pg_user']
pg_pw = postgres_settings['pg_pw']
pg_database = postgres_settings['pg_database']
pg_port_num = postgres_settings['pg_port_num']

def pg_connect():
    """
    Signs in to the Postgres database specified in the global tab_server_pg_db variable.
    Returns a cursor with an open connection for querying tables in the workgroup database.
    """
    # Define our connection string
    global conn_string
    conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % (tab_server_pg_db,pg_database,pg_user,pg_pw,pg_port_num)

    # print the connection string we will use to connect
    print "Connecting to database\n	->host:%s, dbname:%s, port:%s" % (tab_server_pg_db, pg_database, pg_port_num)

    # get a connection, if a connect cannot be made an exception will be raised here
    global conn
    try:
        conn = psycopg2.connect(conn_string)
    except Exception as err:
        print "Unexpected error while establishing connection:{}".format(err)
        sys.exit(1)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    global cursor
    cursor = conn.cursor()
    print "Connected!\n"

    return cursor
