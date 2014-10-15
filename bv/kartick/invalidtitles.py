#! /usr/bin/python
import random

if __name__ == '__main__':
    """fname = 'validupcs.tsv'
    lines = open( fname, 'r' ).readlines()
    invalidtitlecount = 0
    for line in lines:
        words = line.split( '\t' )
        ls = words[:19]
        rs = words[19:]

        if ls[4] == 'NA':
            invalidtitlecount += 1

    print invalidtitlecount"""

    fname = 'jaccard_similarity_0.7_new.tsv'
    lines = open( fname, 'r' ).readlines()
    randomi = [ int(len(lines)*random.random())\
                for i in range(200) ]

    with open( 'random_jaccard_0.7.tsv', 'w' ) as rand:
        for i in randomi:
            words = lines[i].split( '\t' )
            ls = words[:19]
            rs = words[19:]
            rand.write( ls[4] + ' ||||| ' + rs[4] + '\n' )
