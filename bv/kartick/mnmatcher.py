#! /usr/bin/python

import sys
import re

localfile = 'sourceRecords.tsv'
#localfile = 'destinationTesterFile.tsv'

def readLocalFile( localfile ):
    tokensList = []
    lines = open( localfile, 'r' ).readlines()
    for line in lines:
        line = line.strip()
        title = line.split( '\t' )[4]
        title = title.split()
        title = [ cleanTokens(x) for x in title ]
        title = [ x for x in title if x != '' ]
        tokensList.append( title )
    return zip( lines, tokensList )

def createInvIndexTable( localfile ):
    tokensHashTable = {}
    lines = open( localfile, 'r' ).readlines()
    lineswlineno = zip( range(len(lines)), lines )
    for lineno, line in lineswlineno:
        line = line.strip()
        title = line.split( '\t' )[4]
        titleTokens = title.split()
        titleTokens = [ cleanTokens(x)\
                        for x in titleTokens ]
        titleTokens = [ x for x in titleTokens\
                        if x != '' ]
        for token in titleTokens:
            try:
                tokensHashTable[token].append( lineno )
            except:
                tokensHashTable[token] = [ lineno ]
    return tokensHashTable

def cleanTokens( token ):
    regex = ',|\'|\"|\(|\)|\-|\/|\:'
    token = token.lower()
    return re.sub( regex, '' , token )

def removeStopWords( tokens ):
    stopwords = ['a', 'the', 'in', 'for', 'is',
                 'an', 'if', 'of', 'he', 'she', 'it',
                 'on', 'to', 'are', 'was', 'and', 'with' ]
    return [ token for token in tokens\
             if token not in stopwords ]

def stringCompare( titles1, titles2 ):
    """tokens1 = [ cleanTokens(x) for x in\
                title1 ]
    tokens2 = [ cleanTokens(x) for x in\
                title2 ]
    tokens1 = set( [ x for x in\
                     tokens1 if x != '' ] )
    tokens2 = set( [ x for x in\
                     tokens2 if x != '' ] )"""
    tokens1 = set( titles1 )
    tokens2 = set( titles2 )
    intnum = len(tokens1.intersection( tokens2 ))
    unnum = len(tokens1.union( tokens2 ))
    if unnum == 0:
        return 0
    else:
        return float(intnum)/unnum

def lookUpInInvIndTable( tokens ):
    global invIndTable
    problineList = []
    for token in tokens:
        try:
            problineList.extend( invIndTable[token] )
        except:
            pass
    return list( set(problineList) )

localFileData = readLocalFile( localfile )
invIndTable = createInvIndexTable( localfile )
lookUpLinesLens = []

for line in sys.stdin:
    line = line.strip()
    title =  line.split( '\t' )[4]

    titleTokens = title.split()
    titleTokens = [ cleanTokens(x)\
                    for x in titleTokens ]
    titleTokens = [ x for x in titleTokens\
                    if x != '' ]

    lookUpLines = lookUpInInvIndTable( removeStopWords( titleTokens ) )
    lookUpLinesLens.append( len( lookUpLines ) )
    print len( lookUpLines ), sum(lookUpLinesLens)/(len(lookUpLinesLens) + 0.0 ), len(lookUpLinesLens)


    for lineno in lookUpLines:
        ( localline, tokens ) = localFileData[lineno]
        score = stringCompare( tokens, titleTokens )
        #if score > 0.7:
        #    print '\n%s\t%s\t%s' %( line, localline.strip(),str(score)  )
