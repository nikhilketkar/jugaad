from gevent import monkey
monkey.patch_all()

import urllib2

opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'proxy.production.indix.tv:8080'}))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]                                                         
urllib2.install_opener(opener)           

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
    def __init__(self):
        self.cleanup()

    def fetch(self, url):
        try:
            res = urllib2.urlopen(url)
            htmlPage = res.read()                    
            self.htmlPages.append((url, htmlPage))
        except Exception as e:
            sys.stderr.write("ERROR\tFETCHER\t" + url + "\t" + str(e) + "\n")
    
    def cleanup(self):
        self.htmlPages = []
        
    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.htmlPages

inputFilename = sys.argv[1]
outputDirectory = sys.argv[2]

with open(sys.argv[1]) as inputFile:
    lines = inputFile.readlines()
records = [i.strip() for i in lines]
batchFetcher = BatchFetcher()
fileCounter = 0
for currBatch in batch(records, 5):
    currWebpages = batchFetcher.fetchBatch(currBatch, 5)
    for record in currWebpages:
        fileCounter += 1
        url = record[0]
        htmlPage = record[1]
        outputFilename = outputDirectory + "/" + str(fileCounter) + ".html"
        with open(outputFilename, 'w') as outputFile: 
            outputFile.write(htmlPage)
        sys.stderr.write("SUCCESS\t" + url + "\t" + outputFilename + "\n" )
