# initialize_db.py

"""
initialize the database and tables in the NC_smash4 DB
"""

import mysql.connector
from subprocess import call
from numpy import loadtxt

# connect to mysql
cnx = mysql.connector.connect(option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()

# create NC_smash4 database 
cur.execute('create database if not exists nc_smash4;')

# pull in SQL commands from external file to create tables
call('mysql nc_smash4 < init_s4.sql', shell=True)

# fill in seasons table
season_raw = loadtxt('seasons.txt', skiprows=1, dtype='string', delimiter=',')

cur.execute('use nc_smash4;')

for i in xrange(season_raw.shape[0]) :
    season_i = season_raw[i,:]
    cur.execute('insert into seasons (id, start_date, end_date) values (%s, %s, %s);', (int(season_i[0]), str(season_i[1]), str(season_i[2])))

cnx.commit()

cur.close()
cnx.close()
