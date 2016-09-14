# manual_player_merge.py

"""
Despite my best efforts, there will be some players who will enter under wildly different tags that will make it impossible to assign them to the same player id right off the bat.
In this script, we go through and track the changes I am forced to make.

example: Trey Monk usually enters under the name "Haise" but now occasionally enters as "Centipede" or "OneEyedKing".
goal: set "Centipede" and "OneEyedKing" p_id equal to "Haise" p_id

now we can easily select all of Trey Monk's results by searching for the IDs associated with his p_id (which we can find by searching for any of his tags)
select id from players where p_id = <Trey's p_id>
use IDs returned from previous query to trace back his challonge tag ID for each tournament, which leads to his sets.

if it ever turns out that we falsely merged players that should not have been merged, you can revert it by simply setting the p_id to their auto incremented and guaranteed to be unique id.
"""

import mysql.connector

def merge_p1_p2(p1, p2) :
    cur.execute('select p_id from players where main_tag = %s ;', (str(p1) ,))
    p_id = cur.fetchone()[0]
    try : 
        cur.fetchall() # flush cursor in case of duplicate
    except mysql.connector.errors.InterfaceError :
        pass # if cursor was already empty, just proceed
    cur.execute('update players set p_id = %s where main_tag = %s ;', (p_id, str(p2)))
    cnx.commit()

# connect to db
cnx = mysql.connector.connect(database='nc_smash4', option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()

merge_p1_p2('deepblue', 'deep blue')
merge_p1_p2('haise', 'oneeyedking')
merge_p1_p2('kwam', 'wes')
merge_p1_p2('arronator', 'arronater')

merge_p1_p2('haise', 'centipede')
merge_p1_p2('loch', 'md')
merge_p1_p2('stumpy', 'jakop')
# close connection to db
cur.close()
cnx.close()