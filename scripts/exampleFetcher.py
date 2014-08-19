from gevent import monkey
monkey.patch_all()

import urllib2
import lxml.html

import sys

from gevent.pool import Pool

class BatchFetcher:
    def __init__(self):
        self.cleanup()
    def fetch(self, url):
        try:
            res = urllib2.urlopen(url)
            htmlPage = res.read()                    
            self.htmlPages.append((url, htmlPage))
            sys.stderr.write("FETCH_SUCCESS\t" + url + "\n")
        except Exception as e:
            sys.stderr.write("FETCH_FAIL\t" + url + "\t" + str(e) + "\n")
    def cleanup(self):
        self.htmlPages = []        

    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.htmlPages

if __name__ == "__main__":    
    opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'cam-dev03.production-mr.indix.tv:3128'}))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]                                                         
    urllib2.install_opener(opener)           
    
    urls = []
    with open(sys.argv[1]) as inputFile:
        for line in inputFile:
            urls.append(line.strip())
            sys.stderr.write("INPUT\t" + line)

    batchFetcher = BatchFetcher()
    while(len(urls) > 0):
        currWebpages = batchFetcher.fetchBatch(urls, 50)
        newurls = []
        for htmlPage in currWebpages:
            root = lxml.html.fromstring(htmlPage[1])
            try:
                breadcrumb = " ".join([j.encode('ascii', 'ignore').strip() for j in root.cssselect("#s-result-count")[0].itertext()])
                sys.stderr.write("BREADCRUMB_SUCCESS\t" + breadcrumb + "\t" + htmlPage[0] + "\n")
                resultCount = int(" ".join([i for i in root.cssselect('#s-result-count')[0].itertext()]).replace("\n","").strip().split('of')[1].split()[0].strip().replace(",",""))
                for i in xrange(1, resultCount%60):
                    sys.stderr.write("OUTPUT\t" + htmlPage + "\t" + htmlPage[0] + "&page=" + i + "\n")
            except:
                sys.stderr.write("BREADCRUMB_FAIL\t" + htmlPage[0] + "\n")
