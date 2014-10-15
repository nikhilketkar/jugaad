#! /usr/bin/python
import re

if __name__ == '__main__':
    fname = 'jaccard_similarity_0.7_new.tsv'
    lines = open( fname, 'r' ).readlines()
    rgx = '([A-Z0-9\-]+)'

    with open( 'modelids_from_jaccardsim.tsv', 'w' ) as outfile:
        for line in lines:
            line = line.strip()
            words = line.split( '\t' )
            ls = words[:19]
            rs = words[19:]
            title = ls[4]
            matches = re.findall( rgx, title )
            possiblem = [ x for x in matches if len(x) > 2 ]
            filtered = []
            for x in possiblem:
                y = re.findall( '[A-Z]+', x )
                #print y,x
                if len(y) != len(x):
                    filtered.append(x)
            outfile.write( ls[4] + ' ' + str(filtered) + '\n')
