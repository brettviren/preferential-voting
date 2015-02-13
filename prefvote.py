#!/usr/bin/env python

import hashlib
from collections import Counter, namedtuple

class Vote(namedtuple('Vote','user phrase ranking')):
    def __str__(self):
        cr = ','.join(self.ranking)
        return '%s,%s,%s' % (self.user, self.phrase, cr)
    def sha1(self):
        h = hashlib.sha1()
        h.update(str(self))
        return h.hexdigest()

def parse_vote(votestr):
    'Parse line in form of: user,phrase,A,B,C into a Vote object'
    user, phrase, ranking = [x.strip() for x in votestr.split(',',2)]
    ranking = tuple([x.strip() for x in ranking.split(',')])
    return Vote(user, phrase, ranking)


def read_votes(filename):
    'Return list of Vote object read from filename.'
    votes = list()
    with open(filename) as fd:
        for line in fd.readlines():
            line = line.strip()
            if not line:
                continue
            sha1, votestr = [x.strip() for x in line.split()]
            vote = parse_vote(votestr)
            if sha1 != vote.sha1():
                print ('Warning: bad checksum on vote: %s' % vote)
            votes.append(vote)
    return votes

def validate_electorate(votes):
    'Check for double voting'
    electorate = set()
    bad = set()
    for vote in votes:
        if vote.user in electorate:
            print ('Warning, double voting by %s' % vote.user)
            bad.add(vote.user)
        electorate.add(vote.user)
    return bad

def voting_round(votes, ignored=None):
    'Apply a voting round by counting numbers of first but not ignored candidates.'
    ignored = ignored or set()
    counter = Counter()
    for vote in votes:
        for candidate in vote.ranking:
            if candidate in ignored:
                continue
            counter[candidate] += 1
            break
    return counter

def majority(counter):
    'Given a candidate vote counter return the majority lead and their votes or None.'
    total = sum(counter.values())
    lead, count = counter.most_common(1)[0]
    if count*2 > total:
        return (lead, count)

def minority(counter):
    'Given a candidate vote counter return a list of minority trailers and their votes.'
    lowest = min(counter.values())
    ret = list()
    for name, count in counter.items():
        if count == lowest:
            ret.append((name, count))
    return ret

def preferential_voting(votes, num_winners):
    winners = list()
    ignored = list()
    while len(winners) < num_winners:
        counter = voting_round(votes, ignored)

        winner = majority(counter)
        if winner:
            winners.append(winner)
            ignored = [w[0] for w in winners]
            continue

        losers = minority(counter)
        for loser, count in losers:
            ignored.append(loser)
        continue
    return winners

def test():
    votes = list()
    counter = Counter(dict(ABC=8, ACB=26, BCA=20, BAC=17, CAB=20, CBA=9))
    for count,rank in enumerate(counter.elements()):
        user = 'voter%02d' % count
        phrase = 'phrase%03d' % count
        vote = Vote(user,phrase,rank)
        votes.append(vote)

    winners = preferential_voting(votes, 2)
    print winners


test()
