#! /usr/bin/python
import re
from multiprocessing import Pool

#fname = 'highConfidenceMatches.tsv'
#fname = 'outputmerged'
fname = 'potentialMatches.tsv'

indx = { 3 : "SKU" ,
         11 : "UPC",
         12 : "EAN", 
         13 : "GTIN",
         14 : "ModelNUM",
         15 : "MPN",
         16 : "ISBN" }

def cleantokens( token ):
    regex = ',|\'|\"|\(|\)|\-|\/|\:'
    token = token.lower()
    return re.sub( regex, ' ' , token )
    
def comparetitles( title1, title2 ):
    tokens1 = [ cleantokens(x) for x in\
                title1.split( ' ' )]
    tokens2 = [ cleantokens(x) for x in\
                title2.split( ' ' )]
    tokens1 = set( [ x for x in\
                     tokens1 if x != '' ] )
    tokens2 = set( [ x for x in\
                     tokens2 if x != '' ] )
    intnum = len(tokens1.intersection( tokens2 ))
    unnum = len(tokens1.union( tokens2 ))
    if unnum == 0:
        return 0
    else:
        return float(intnum)/unnum

def comparetitles2( title1, title2 ):
    tokens1 = [ cleantokens(x) for x in\
                title1.split( ' ' )]
    tokens2 = [ cleantokens(x) for x in\
                title2.split( ' ' )]
    tokens1 = set( [ x for x in\
                     tokens1 if x != '' ] )
    tokens2 = set( [ x for x in\
                     tokens2 if x != '' ] )
    intnum = len(tokens1.intersection( tokens2 ))
    unnum = min( len(tokens1), len(tokens2) )
    if unnum == 0:
        return 0
    else:
        return float(intnum)/unnum
        
##########################
# Diff String Similarity
##########################


##########################
# Jaccard Similarity Thresholding
##########################
def filter07( lines ):
    thresholdv = []
    for data in lines:
        ( lineno, line ) = data
        if lineno%100 == 0:
            print lineno
        line = line.strip()
        words = line.split( '\t' )
        ls = words[:19]
        rs = words[19:]
        score = comparetitles( ls[4], rs[4] )
        if score > 0.7:
            thresholdv.append( lineno )
    return thresholdv

def finisher_filter07( results ):
    global linesd
    with open( 'jaccard_similarity_0.5_new.tsv', 'w' ) as outfile:
        for res in results:
            for lineno in res:
                outfile.write( linesd[lineno] )

#########################
# Invalid UPC and valid UPC
#########################

def findinvalidUPC( lines ):
    invalidupcs = []
    validupcs = []
    crazeeupc = []
    for data in lines:
        ( lineno, line ) = data
        if lineno%100 == 0:
            print lineno
        line = line.strip()
        words = line.split( '\t' )
        ls = words[:19]
        rs = words[19:]
        score = comparetitles( ls[4], rs[4] )
        if score > 0.7:
            if ls[11] == '000000000000' or\
               ls[11] == 'NA':
                invalidupcs.append( ( lineno, score ) )
            elif rs[11] == '000000000000' or\
                 rs[11] == 'NA':
                invalidupcs.append( ( lineno, score ) )
            elif ls[11] == rs[11]:
                validupcs.append( ( lineno, score ) )
            elif ls[11] != rs[11]:
                crazeeupc.append( ( lineno, score ) )
    return ( invalidupcs, validupcs, crazeeupc )

def finisher_findinvalidUPC( results ):
    global linesd
    totalinvalid = []
    totalvalid = []
    totalcrazee = []

    for result in results:
        ( invalid, valid, crazee ) = result
        totalinvalid.extend( invalid )
        totalvalid.extend( valid )
        totalcrazee.extend( crazee )
    
    with open( 'invalidupcs.tsv', 'w' ) as outfile:
        for i, score in totalinvalid:
            outfile.write( linesd[i].strip() + '\t' + str(score) + '\n' )

    with open( 'validupcs.tsv', 'w' ) as outfile:
        for i, score in totalvalid:
            outfile.write( linesd[i].strip() + '\t' + str(score) + '\n' )            
    
    with open( 'crazee.tsv', 'w' ) as outfile:
        for i, score in totalcrazee:
            outfile.write( linesd[i].strip() + '\t' + str(score) + '\n' )

class BazaarVoice():
    
    def __init__( self ):
        self.n = 10

    def makeparts( self, data, n ):
        step = len(data)/n
        part = range( 0, len(data), step )
        data2 = zip( range( len(data) ), data )
        parts = [ data2[part[i]:part[i+1]]\
                  for i in range( 0, len(part) - 1 ) ]
        if part[-1] < len( data2 ):
            parts.append( data2[part[-1]:-1] )

        return parts

    def run( self , processer, finisher, data ):
        global lines
        processpool = Pool(processes=self.n)
        results = processpool.map( processer, data )
        finisher( results )
        
if __name__ == '__main__':
    linesd = open( fname, 'r' ).readlines()
    print len(linesd)

    bv = BazaarVoice()
    bv.run( filter07, finisher_filter07 , bv.makeparts( linesd, bv.n ) )
    #bv.run( findinvalidUPC, finisher_findinvalidUPC , bv.makeparts( linesd, bv.n ) )
