from gevent import monkey
monkey.patch_all()

import urllib2
import lxml.html

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

    def fetch(self, record):
        try:
            AMAZON_TITLE, AMAZON_MARKETPLACE_TITLE, AMAZON_URL, AMAZON_MARKETPLACE_URL, DRUGSTORE_URL = record.split('\t')
            if AMAZON_TITLE == "NA":
                currTitle = AMAZON_MARKETPLACE_TITLE
            else:
                currTitle = AMAZON_TITLE            

            searchUrl = "http://www.amazon.com/s/&field-keywords=" + urllib2.quote(currTitle)            
            searchPage = urllib2.urlopen(searchUrl).read()
            root = lxml.html.fromstring(searchPage)

            try:
                leafUrl = "http://www.amazon.com" + root.cssselect('.childRefinementLink')[0].getparent().attrib['href']
            except:
                leafUrl = "http://www.amazon.com" + root.cssselect('.boldRefinementLink')[0].getparent().attrib['href']

            leafPage = urllib2.urlopen(leafUrl).read()
            root = lxml.html.fromstring(leafPage)
            facets = "|".join([i.text.replace("\t","").replace("\n", "") for i in root.cssselect('.refinementLink')])
            sys.stdout.write("SUCCESS\t" + record.strip() + "\t"+ facets + "\n")            
        except Exception as e:
            sys.stdout.write("ERROR\t" + record + "\t" + str(e) +  "\n")
    
    def cleanup(self):
        self.htmlPages = []
        
    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.htmlPages

inputFilename = sys.argv[1]

with open(sys.argv[1]) as inputFile:
    lines = inputFile.readlines()
records = [i.strip() for i in lines]
batchFetcher = BatchFetcher()
fileCounter = 0
for currBatch in batch(records, 50):
    currWebpages = batchFetcher.fetchBatch(currBatch, 50)
