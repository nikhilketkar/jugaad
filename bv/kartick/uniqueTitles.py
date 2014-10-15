#! /usr/bin/python

if __name__ == '__main__':
    fname = 'jaccardSimilarity0.7andupcMathces.tsv'
    lines = open( fname , 'r' ).readlines()
    uniqueTitles = {}
    lineszip = zip( range(len(lines)), lines ) 
    for ( lineno, line ) in lineszip:
        line = line.strip()
        words = line.split( '\t' )
        ls = words[:19]
        rs = words[19:]
        try:
            uniqueTitles[ls[4]].append( lineno )
        except:
            uniqueTitles[ls[4]] = [lineno]

    print len( uniqueTitles.keys() )

    with open( 'uniqueTitles' , 'w' ) as outfile:
        for title in uniqueTitles.keys():
            outfile.write( title + ' ' + str(len(uniqueTitles[title])) + '\n' )
                    
    with open( 'uniqueTitleRecords.tsv', 'w' ) as outfile:
        for title in uniqueTitles.keys():
            outfile.write( lines[uniqueTitles[title][0]] )
