from gevent import monkey
monkey.patch_all()

import urllib2
import lxml.html

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
            sys.stderr.write("SUCCESS\tFETCHER\t" + url + "\n")
        except Exception as e:
            sys.stderr.write("ERROR\tFETCHER\t" + url + "\t" + str(e) + "\n")
    
    def cleanup(self):
        self.htmlPages = []
        
    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.htmlPages

opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'proxy.production.indix.tv:8080'}))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]                                                         
urllib2.install_opener(opener)           

url = "http://www.amazon.com/"
res = urllib2.urlopen(url)
htmlPage = res.read()                    
root = lxml.html.fromstring(htmlPage)
searchAliases = [i.attrib["value"] for i in root.cssselect('.searchSelect')[0].getchildren()]
urls = ["http://www.amazon.com/s/ref=nb_sb_noss?url=" + urllib2.quote(i) + "&field-keywords=" for i in searchAliases if i != "search-alias=aps"]

batchFetcher = BatchFetcher()
while(len(urls) > 0):
    currWebpages = batchFetcher.fetchBatch(urls, 5)
    newurls = []
    for htmlPage in currWebpages:
        root = lxml.html.fromstring(htmlPage[1])
        try:
            categoryRefinements = root.cssselect('.categoryRefinementsSection')[0]
            currnewurls = ["http://www.amazon.com/" + i.getparent().attrib['href'] for i in categoryRefinements.cssselect('.refinementLink')]
            newurls.extend(currnewurls)
        except:
            print "Expansion Stopped for " + htmlPage[0]
        try:
            breadcrumb = " ".join([j.encode('ascii', 'ignore').strip() for j in root.cssselect("#s-result-count")[0].itertext()])
            print breadcrumb
        except:
            print "No breadcrumb for " + htmlPage[0]
    urls = newurls
    