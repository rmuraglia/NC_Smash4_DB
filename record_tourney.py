# record_tourney.py

"""
insert the results from a single tourney from challonge into the db
"""

import mysql.connector
import challonge
from pprint import pprint
import re
import urllib2
import sys
import numpy as np
import datetime

# get my challonge credentials from file
creds = {}
with open('challonge_credentials.txt') as f :
    for _ in xrange(2) : # skip first two lines
        next(f)
    for line in f :
        (key, val) = line.split()
        creds[key] = val
challonge.set_credentials(creds['user'], creds['api_key'])

# define tourney of interest
tourney_url = raw_input("Please input the full tournament URL, including the http:// \n")
t_split = re.split('[\.\/]', tourney_url) # split on periods and forward slashes
challonge_ind = t_split.index('challonge')
if t_split[challonge_ind-1] == '' :
    # this means there is no subdomain on the challonge url
    t_name = t_split[challonge_ind+2]
else :
    t_name = t_split[challonge_ind-1] + '-' + t_split[challonge_ind+2]

# load tournament information
try :
    tournament = challonge.tournaments.show(t_name)
except urllib2.HTTPError as err :
    print err
    print 'Unable to fetch tournament information'
    print 'Exiting script...'
    sys.exit(1)

# load participants information
try:
    participants = challonge.participants.index(t_name)
except urllib2.HTTPError as err :
    print err
    print 'Unable to fetch participant information'
    print 'Exiting script...'
    sys.exit(1)

# load set information
try:
    matches = challonge.matches.index(t_name)
except urllib2.HTTPError as err :
    print err
    print 'Unable to fetch match information'
    print 'Exiting script...'
    sys.exit(1)

# load in season start/end info
season_raw = np.loadtxt('seasons.txt', skiprows=1, dtype='string', delimiter=',')

def season_parse(season_string) :
    season_ints = [int(x) for x in season_string.split('/')]
    return datetime.date(season_ints[0], season_ints[1], season_ints[2])

season_dates = [season_parse(x) for x in season_raw[:,2]] # get all season end dates
season_dates.append(datetime.date.today()) # add today's date as final possible date for tournament
season_dates.insert(0, datetime.date(2014, 11, 01)) # add first known tournament for start of season 1
season_dates.insert(0, datetime.date(2014, 10, 03)) # add 3DS release date as first possible date for tournament (season 0)

# example of how to get season
test_date = tournament['started-at'].date()
season_id = [i for i in xrange(11) if season_dates[i]<test_date<=season_dates[i+1]][0]
print season_id

# connect to db
cnx = mysql.connector.connect(database='nc_smash4', option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()







# close connection to db
cur.close()
cnx.close()