from gevent import monkey
monkey.patch_all()

import urllib2
import lxml.html

import sys

from gevent.pool import Pool

opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'cam-dev03.production-mr.indix.tv:3128'}))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]                                                         
urllib2.install_opener(opener)           

def getPage(url):
    res = urllib2.urlopen(url)
    htmlPage = res.read()                    
    return lxml.html.fromstring(htmlPage)

def getTotalResults(root):
    searchResultLine = root.cssselect('#s-result-count')[0].text
    words = searchResultLine.split()
    if len(words) == 5:
        return int(words[2].replace(',',""))
    elif len(words) == 3:
        return int(words[0].replace(',',""))

def getMostSpecificRefinement(root):
    return root.cssselect("#s-result-info-bar")[0].cssselect('.a-color-state')[0].text.encode('ascii', 'ignore')

def getProductURLs(root):
    return [i.cssselect('a')[0].attrib["href"] for i in root.cssselect('#resultsCol')[0].cssselect('.newaps')]

def extractASINs(urls):
    return [i.replace("dp/","\t").replace("/ref","\t").split('\t')[1] for i in urls]

def getRefinementAndURLs(facetName, url):
    root = getPage(url)
    refinement = getMostSpecificRefinement(root)
    productCount = getTotalResults(root)
    productsPerPage = 24
    urls = [url + "&page=" + str(i) for i in xrange(1, productCount/productsPerPage + 2)]
    for i in urls:
        sys.stderr.write("SEEDED" + "\t" + i + "\t" + refinement + "\t" + facetName + "\n")
    return refinement, urls

def getProducts(url):
    root = getPage(url)
    productURLs = getProductURLs(root)
    return extractASINs(productURLs)

def getAProducts(facetName, url):
    refinement, urls = getRefinementAndURLs(facetName, url)
    ASINS = []
    for url in urls:
        currASINS = getProducts(url)
        for asin in currASINS:
            sys.stderr.write("RESULT" + "\t" + facetName + "\t" + refinement + "\t" + asin + "\n")
        ASINS.extend(currASINS)
        sys.stderr.write("PROCESSED" + "\t" + url  +  "\n")

def processRecord(record):
    facet, url = record
    getAProducts(facet, url)

poolSize = int(sys.argv[2])
with open(sys.argv[1]) as inputFile: lines = inputFile.readlines()
records = [i.strip().split('|') for i in lines]
pool = Pool(min(len(records), poolSize))
pool.map(processRecord, records)

