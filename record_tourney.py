# record_tourney.py

"""
insert the results from a single tourney from challonge into the db
"""

import mysql.connector
import challonge
from pprint import pprint

cnx = mysql.connector.connect(database='nc_smash4', option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()


cur.close()
cnx.close()