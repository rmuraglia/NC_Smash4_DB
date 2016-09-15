# inspect_set.py

import pickle
from pprint import pprint

tourney_name = 'SSF0613' # change this line to inspect a given tournament
 
with open('dat/' + tourney_name + '/matches.pickle', 'rb') as f : all_matches = pickle.load(f)

with open('dat/' + tourney_name + '/inspect_sets.log', 'rb') as f : query_matches = f.readlines()

query_matches = [int(x) for x in query_matches]

all_match_ids = [x['id'] for x in all_matches]

for query in query_matches :
    query_ind = [x==query for x in all_match_ids].index(True)
    print '\n'
    pprint(all_matches[query_ind])

