import sys
import urllib2

def genASearchURL(searchPhrase):
    return "http://www.amazon.com/s/&field-keywords=" + urllib2.quote(searchPhrase)

for line in sys.stdin:
    DS_WALGREEN_URL, AMAZON_MARKETPLACE_URL, TITLE, STORE_ID = line.strip().split('\t')
    result = [DS_WALGREEN_URL, AMAZON_MARKETPLACE_URL, TITLE, STORE_ID, genASearchURL(TITLE)]
    sys.stdout.write("\t".join(result) + "\n")

