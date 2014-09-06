from gevent import monkey
monkey.patch_all()

import urllib2
import unirest

import sys

from gevent.pool import Pool

def batch(givenList, batchSize):
    consumedUpto = 0
    while consumedUpto < len(givenList):
        currBatch = []
        while len(currBatch) < batchSize and consumedUpto < len(givenList):
            currBatch.append(givenList[consumedUpto])
            consumedUpto += 1
        yield currBatch

class BatchFetcher:
    def __init__(self, key):
        self.cleanup()
        self.key = key

    def fetch(self, url):
        try:
            crawleraEndpoint = "https://crawlera.p.mashape.com/fetch?url="
            quoteURL = urllib2.quote(url)
            fetchurl = crawleraEndpoint + quoteURL
            response = unirest.get(fetchurl, headers={"X-Mashape-Key": self.key})            
            self.htmlPages.append((url, response))
        except Exception as e:
            sys.stderr.write("ERROR\t" + url + "\t" + str(e) + "\n")
    
    def cleanup(self):
        self.htmlPages = []
        
    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.htmlPages

inputFilename = sys.argv[1]
outputDirectory = sys.argv[2]
key = sys.argv[3]
batchSize = int(sys.argv[4])
poolSize = int(sys.argv[5])

with open(inputFilename) as inputFile:
    lines = inputFile.readlines()
records = [i.strip() for i in lines]
batchFetcher = BatchFetcher(key)
fileCounter = 0
for currBatch in batch(records, batchSize):
    currWebpages = batchFetcher.fetchBatch(currBatch, poolSize)
    for record in currWebpages:
        fileCounter += 1
        url = record[0]
        htmlPage = record[1].body
        outputFilename = outputDirectory + "/" + str(fileCounter) + ".html"
        with open(outputFilename, 'w') as outputFile: 
            outputFile.write(htmlPage)
        sys.stderr.write("SUCCESS\t" + url + "\t" + outputFilename + "\n" )
