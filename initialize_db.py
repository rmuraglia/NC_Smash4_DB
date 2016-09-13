# initialize_db.py

"""
initialize the database and tables in the NC_smash4 DB
"""

import mysql.connector
from subprocess import call

# connect to mysql
cnx = mysql.connector.connect(option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()

# create NC_smash4 database 
cur.execute('create database if not exists nc_smash4;')

# pull in SQL commands from external file
call('mysql nc_smash4 < init_s4.mysql', shell=True)

cur.close()
cnx.close()
