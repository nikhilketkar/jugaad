#! /usr/bin/python

if __name__ == '__main__':
    fname = 'jaccard_similarity_0.7_new.tsv'
    lines = open( fname, 'r' ).readlines()
    with open( 'filtered_jaccard_similarity_0.7.tsv', 'w' ) as outfile:
        for line in lines:
            linest = line.strip()
            words = linest.split( '\t' )
            ls = words[:19]
            rs = words[19:]
            if ls[4] != 'NA':
                outfile.write( line )
            
