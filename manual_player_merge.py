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

merge_p1_p2('haise', 'sasaki')
merge_p1_p2('zepdragon', 'zeppdragon')

merge_p1_p2('the spoon broom', 'the spoonbroom')
merge_p1_p2('yungz', 'yungsz')
merge_p1_p2('kdogg', 'kdawgg')
merge_p1_p2('ohboyhowdy', 'oh boy howdy!')

merge_p1_p2('putthatcookiedown', 'puthatcookiedown')
merge_p1_p2('The Zone', 'TheZone')
merge_p1_p2('Pidgey', 'Bayonettamaster23')

merge_p1_p2('thibault', 'thatguy')
merge_p1_p2('leaf fc', 'leaffc')

merge_p1_p2('l.v. mises', 'l.v.mises')
merge_p1_p2('luke nasty', 'lukenasty')

merge_p1_p2('GokuGuy', 'SGT|Goku')
merge_p1_p2('Dublio', 'Oilbud')
merge_p1_p2('Kaneki', "Hisoka's buttcheeks")
merge_p1_p2('cakesofspan', 'cakesofpan')

merge_p1_p2('ohboyhowdy', 'oh boyhowdy')

merge_p1_p2('haise', 'hanzogod24')

# merge_p1_p2('arago', 'tank') # verify?

merge_p1_p2('stingers', 'tracergod69')
merge_p1_p2('donquavious', 'donquaviswiss')
merge_p1_p2('who-z', 'Loozy')

merge_p1_p2('Dandy Penguin', "Tom Clancy's The Penguin")

merge_p1_p2('sideB', 'side B')

merge_p1_p2('the white glove special', 'whiteglovespecial')

merge_p1_p2('Syde7', 'REIGN')
merge_p1_p2('revan', 'yo$hig0d')

merge_p1_p2('prince ali', 'prince ali fabulous he ali ababwa')

merge_p1_p2('haise', 'arima')
merge_p1_p2('Musk Ox', 'MuskOx')
merge_p1_p2('lazymp', 'YerBoiMP')

merge_p1_p2('Dandy Penguin', 'Oswald Cobblepot')
merge_p1_p2('thibault', 'mike jones')

merge_p1_p2('revan', 'sonicman')
merge_p1_p2('haise', 'artorias')
merge_p1_p2('l.v. mises', 'l.v mises')
merge_p1_p2('the dorf', 'highti3rg0d')

merge_p1_p2('deepblue', 'big blu')

merge_p1_p2('the dorf', 'hidden sleeper')

# close connection to db
cur.close()
cnx.close()