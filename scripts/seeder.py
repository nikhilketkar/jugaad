from gevent import monkey
monkey.patch_all()

import urllib2
import lxml.html

import sys

from gevent.pool import Pool

opener = urllib2.build_opener(urllib2.ProxyHandler({'http': 'cam-dev03.production-mr.indix.tv:3128'}))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36')]                                                       
urllib2.install_opener(opener)           

def extractURLs(url, htmlPage):
    newurls = []
    root = lxml.html.fromstring(htmlPage)
    try:
        categoryRefinements = root.cssselect('.categoryRefinementsSection')[0]
        newurls = ["http://www.amazon.com/" + i.getparent().attrib['href'] for i in categoryRefinements.cssselect('.refinementLink')]
    except:
        sys.stderr.write("EXPANSION_STOP\t" + url + "\n")
    try:
        breadcrumb = " ".join([j.encode('ascii', 'ignore').strip() for j in root.cssselect("#s-result-count")[0].itertext()])
        sys.stderr.write("BREADCRUMB_SUCCESS\t" + breadcrumb + "\t" + url + "\n")
    except:
        sys.stderr.write("BREADCRUMB_FAIL\t" + url + "\n")
    return newurls

def getPage(url):
    res = urllib2.urlopen(url)
    htmlPage = res.read()                    
    return htmlPage

class BatchFetcher:
    def __init__(self):
        self.cleanup()
    def fetch(self, url):
        try:
            res = urllib2.urlopen(url)
            htmlPage = res.read()                    
            self.newurls.extend(extractURLs(url, getPage(url)))
            sys.stderr.write("PROCESS_SUCCESS\t" + url + "\n")
        except Exception as e:
            sys.stderr.write("PROCESS_FAIL\t" + url + "\t" + str(e) + "\n")
    def cleanup(self):
        self.newurls = []        

    def fetchBatch(self, urls, poolSize):
        self.cleanup()
        pool = Pool(min(len(urls), poolSize))
        pool.map(self.fetch, urls)
        return self.newurls

"""
<option selected="selected" value="search-alias=aps">All Departments</option>
<option value="search-alias=instant-video">Amazon Instant Video</option>
<option value="search-alias=appliances">Appliances</option>
<option value="search-alias=mobile-apps">Apps & Games</option>
<option value="search-alias=arts-crafts">Arts, Crafts & Sewing</option>
<option value="search-alias=automotive">Automotive</option>
<option value="search-alias=baby-products">Baby</option>
<option value="search-alias=beauty">Beauty</option>
<option value="search-alias=stripbooks">Books</option>
<option value="search-alias=popular">CDs & Vinyl</option>
<option value="search-alias=mobile">Cell Phones & Accessories</option>
<option value="search-alias=fashion">Clothing, Shoes & Jewelry</option>
<option value="search-alias=fashion-womens">&#160;&#160;&#160;Women</option>
<option value="search-alias=fashion-mens">&#160;&#160;&#160;Men</option>
<option value="search-alias=fashion-girls">&#160;&#160;&#160;Girls</option>
<option value="search-alias=fashion-boys">&#160;&#160;&#160;Boys</option>
<option value="search-alias=fashion-baby">&#160;&#160;&#160;Baby</option>
<option value="search-alias=collectibles">Collectibles & Fine Art</option>
<option value="search-alias=computers">Computers</option>
<option value="search-alias=financial">Credit and Payment Cards</option>
<option value="search-alias=digital-music">Digital Music</option>
<option value="search-alias=electronics">Electronics</option>
<option value="search-alias=gift-cards">Gift Cards Store</option>
<option value="search-alias=grocery">Grocery & Gourmet Food</option>
<option value="search-alias=hpc">Health & Personal Care</option>
<option value="search-alias=garden">Home & Kitchen</option>
<option value="search-alias=industrial">Industrial & Scientific</option>
<option value="search-alias=digital-text">Kindle Store</option>
<option value="search-alias=fashion-luggage">Luggage & Travel Gear</option>
<option value="search-alias=magazines">Magazine Subscriptions</option>
<option value="search-alias=movies-tv">Movies & TV</option>
<option value="search-alias=mi">Musical Instruments</option>
<option value="search-alias=office-products">Office Products</option>
<option value="search-alias=lawngarden">Patio, Lawn & Garden</option>
<option value="search-alias=pets">Pet Supplies</option>
<option value="search-alias=pantry">Prime Pantry</option>
<option value="search-alias=software">Software</option>
<option value="search-alias=sporting">Sports & Outdoors</option>
<option value="search-alias=tools">Tools & Home Improvement</option>
<option value="search-alias=toys-and-games">Toys & Games</option>
<option value="search-alias=videogames">Video Games</option>
<option value="search-alias=wine">Wine</option>
"""

selectedCategories = ["search-alias=hpc",\
                      "search-alias=grocery",\
                      "search-alias=beauty",\
                      "search-alias=baby-products",\
                      "search-alias=toys-and-games",\
                      "search-alias=pets",\
                      "search-alias=garden"]

if __name__ == "__main__":    
    poolSize = int(sys.argv[1])    
    url = "http://www.amazon.com/"
    res = urllib2.urlopen(url)
    htmlPage = res.read()                    
    root = lxml.html.fromstring(htmlPage)
    searchAliases = [i.attrib["value"] for i in root.cssselect('.searchSelect')[0].getchildren()]
    urls = ["http://www.amazon.com/s/ref=nb_sb_noss?url=" + urllib2.quote(i) + "&field-keywords=" for i in searchAliases if i in selectedCategories]
    for url in urls:
        sys.stderr.write("SEEDED\t" + url + "\n")
    batchFetcher = BatchFetcher()
    while(len(urls) > 0):
        urls = batchFetcher.fetchBatch(urls, poolSize)
        for url in urls:
            sys.stderr.write("SEEDED\t" + url + "\n")
    
