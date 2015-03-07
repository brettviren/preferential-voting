#!/usr/bin/env python

import hashlib
import random
from collections import Counter


test_weighted_ballots = [('ABC',  8), 
                         ('ACB', 26),
                         ('BCA', 20),
                         ('BAC', 17),
                         ('CAB', 20),
                         ('CBA',  9)]
votes = Counter()
for rank,weight in test_weighted_ballots:
    votes[rank] += weight
#print votes

def make_vote(user_name,voter_phrase,candidate_ranking):
    cr = ','.join(candidate_ranking)
    return '%s,%s,%s' % (user_name, voter_phrase, cr)



for count,rank in enumerate(votes.elements()):
    user = 'voter%02d' % count
    phrase = 'phrase%03d' % random.randint(0,999)
    vote = make_vote(user,phrase,rank)
    sha1 = hashlib.sha1()
    sha1.update(vote)
    print ('%s %s' % (sha1.hexdigest(), vote))

