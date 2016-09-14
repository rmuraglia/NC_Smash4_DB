# import_one_tournament.py

"""
take as input one tournament URL and populate players, tags, tourneys, sets and player-tourney junction table
"""

import mysql.connector
import challonge
import urllib2
from pprint import pprint
import re
import sys
import datetime

"""
Part 1: import tourney data from API
"""

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
    print 'Tournament record successfully imported'
except urllib2.HTTPError as err :
    print err
    print 'Unable to fetch tournament information'
    print 'Exiting script...'
    sys.exit(1)

# if tournament is not complete, then exit script with warning
if tournament['completed-at'] is None :
    print 'Tournament <' + tournament['name'] + '> was not marked as completed.\n Please verify that this is a tournament you want to import with this script.\n If this represents a bracket pool from a larger tournament, please use a different script.\n Exiting this script without importing any data.'
    sys.exit(1)

# load set information
try :
    matches = challonge.matches.index(t_name)
    print 'Match record successfully imported'
except urllib2.HTTPError as err :
    print err
    print 'Unable to fetch match information'
    print 'Exiting script...'
    sys.exit(1)

# load participants information
try :
    participants = challonge.participants.index(t_name)
    print 'Participant record successfully imported'
except urllib2.HTTPError as err :
    print err
    print 'Unable to fetch participant information'
    print 'Exiting script...'
    sys.exit(1)

# connect to db
cnx = mysql.connector.connect(database='nc_smash4', option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()

""" 
Part 2: Import player and tag information.
Sort through list of challonge tags for tournament and decide which ones are new players, and which are aliases of existing players
Add new uniques to the players table
Add all tags to tags table to map back to unique players
"""

# get list of players already in db
cur.execute('select main_tag from players;')
player_list_raw = cur.fetchall()
player_list = [x[0].lower() for x in player_list_raw]

# helper functions
def new_tag(tag) :
    response = raw_input("No player tag matches found for <" + tag + ">. \n What would you like their players.main_tag entry to be? \n Type your response with no quotes. If you would like to accept this tag as their permanent tag, simply press enter. \n \n")
    if response == '' : return tag.lower()
    else : return response.lower()

def real_name_prompt(tag) :
    response = raw_input("Would you like to assign a real name for <" + tag + ">? \n If so, please type their name with no quotes. If not, simply press enter. \n \n")
    if response == '' : return None
    else : return response

def new_player(tag) :
    main_tag = new_tag(tag)
    real_name = real_name_prompt(tag)
    cur.execute('select max(p_id) from players;')
    last_pid = cur.fetchone()[0]
    if last_pid is None : next_pid = 1 # this is the first entry
    else : next_pid = last_pid + 1
    cur.execute('insert into players (p_id, main_tag, real_name) values (%s, %s, %s);', (next_pid, main_tag, real_name))
    return main_tag

# loop through and process each challonge participant
for participant in participants :

    # check if this participant matches any records in player table
    match_bools = [x in participant['name'].lower() for x in player_list]

    if any(match_bools) : #there was a player-tag match
        best_guess = player_list[match_bools.index(True)]
        keep_match = raw_input("Player tag <" + best_guess + "> is our current guess match for tournament tag <" + participant['name'] + ">. \n Do you accept merging these two tags? \n Please respond with either Y or N, without quotes. \n \n").lower()
        if keep_match=='y': # accept merge - only need entry in tags table
            main_tag = best_guess
        elif keep_match=='n' : # reject merge and make new player record
            main_tag = new_player(participant['name'])
        else : # invalid response for merge - skip this participant
            print "Warning: unclear merging response for tournament tag <" + participant['name'] + ">. \nPlease take note and respond with ONLY Y or N next time. \n"
            continue
    else : # there was no player-tag match
        main_tag = new_player(participant['name'])

    # add new tag record for all participants, new and old
    cur.execute('select id from players where main_tag = %s ;', (main_tag, ))
    p_id = cur.fetchone()[0]
    try : 
        cur.fetchall() # flush cursor in case of duplicate
    except mysql.connector.errors.InterfaceError :
        pass # if cursor was already empty, just proceed
    cur.execute('insert into tags (id, tag, player_id) values (%s, %s, %s);', (participant['id'], participant['name'], p_id))
    cnx.commit()

"""
Part 3: Import tournament information
"""

# get season delimiters
season_dates = []
cur.execute('select end_date from seasons;')
while True :
    try :
        season_dates.append(cur.fetchone()[0])
    except TypeError :
        print 'All season end dates have been fetched and appended'
        break

# add game release as earliest possible day for tournament
cur.execute('select start_date from seasons where id = 0;')
release_date = cur.fetchone()[0]
season_dates.insert(0, release_date)

def get_season(tourney_date, season_dates) :
    if tourney_date < season_dates[0] :
        print "Tourney date appears to be before game's release."
        print "Please double check your date"
        return None
    elif tourney_date > season_dates[-1] :
        print "Tourney date appears to be after end of current season."
        print "Please double check that seasons table is up to date with current season."
        return None
    else :
        season_id = [i for i in xrange(len(season_dates)) if season_dates[i]<tourney_date<=season_dates[i+1]][0]
        return season_id

t_id = tournament['id']
t_title = tournament['name']
t_date = tournament['started-at'].date()
t_season = get_season(t_date, season_dates)
t_num_entrants = tournament['participants-count']
t_url = tournament['full-challonge-url']
cur.execute('insert into tournaments (id, title, tourney_date, season, num_entrants, url) values (%s, %s, %s, %s, %s, %s);', (t_id, t_title, t_date, t_season, t_num_entrants, t_url))
cnx.commit()

"""
Part 4: Import set information
"""

# helper functions
def get_winner(sc1, sc2, id) :
    if sc1 < sc2 : 
        return 2
    elif sc1 > sc2 : 
        return 1
    else : 
        print "Warning: a winner cannot be determined for set <" + str(id) + ">. Please verify this set's results." 
        return None

def parse_scores_csv(match) :
    score_split = match['scores-csv'].split('-')
    if len(score_split)==2 : # this is a regular score
        sc1 = int(score_split[0])
        sc2 = int(score_split[1])
        w = get_winner(sc1, sc2, match['id'])
    elif len(score_split)==3 : # this means someone got DQed, or forfeited and was awared a negative game count
        neg_ind = [''==x for x in score_split].index(True)
        if neg_ind==0 :
            sc1 = -int(score_split[1])
            sc2 = int(score_split[2])
        elif neg_ind==1 :
            sc1 = int(score_split[0])
            sc2 = -int(score_split[2])
        else : 
            print "Warning: there was an abnormal game count for set <" + match['id'] + ">. Please verify this set's results."
            return [None, None, None]
        w = get_winner(sc1, sc2, match['id'])
    else :
        print "Warning: there was an abnormal game count for set <" + match['id'] + ">. Please verify this set's results."
        return [None, None, None]
    return [sc1, sc2, w]

for match in matches :
    s_id = match['id']
    s_t_id = match['tournament-id']
    s_round = match['round']
    p1_id = match['player1-id']
    p2_id = match['player2-id']
    sc = parse_scores_csv(match)
    p1_sc = sc[0]
    p2_sc = sc[1]
    s_w = sc[2]
    p1_prev = match['player1-prereq-match-id']
    p2_prev = match['player2-prereq-match-id']
    p1_pl = match['player1-is-prereq-match-loser']
    p2_pl = match['player2-is-prereq-match-loser']
    cur.execute('insert into sets (id, tourney_id, round, p1_id, p2_id, p1_score, p2_score, winner, p1_prev_set, p2_prev_set, p1_prev_lose, p2_prev_lose) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);', (s_id, s_t_id, s_round, p1_id, p2_id, p1_sc, p2_sc, s_w, p1_prev, p2_prev, p1_pl, p2_pl))
    cnx.commit()

"""
Part 5: Populate player-tourney junction table
"""

for participant in participants :
    cur.execute('select player_id from tags where id = %s ;', (participant['id'],))
    p_id = cur.fetchone()[0]
    t_id = participant['tournament-id'] 
    p_seed = participant['seed']
    p_f_rank = participant['final-rank']
    cur.execute('insert into player_tournament_junction (tourney_id, player_id, seed, final_rank) values (%s, %s, %s, %s);', (t_id, p_id, p_seed, p_f_rank))
    cnx.commit()

# close connection to db
cur.close()
cnx.close()