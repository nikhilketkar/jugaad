import sys
import urllib2

def genPrefix():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789 ?'
    for i in alphabet:
        for j in alphabet:
            for k in alphabet:
                yield (i+j+k).replace("?","")

prefixSet = set([])
for prefix in genPrefix():
    prefixSet.add(prefix)

with open(sys.argv[2],'w') as outputFile:
    for prefix in prefixSet:
        if sys.argv[1] == "amazon":
            url = "http://completion.amazon.com/search/complete?method=completion&q=" + urllib2.quote(prefix) + "&search-alias=aps&client=amazon-search-ui&mkt=1"
        elif sys.argv[1] == "shopping":
            url = "http://www.shopping.com/ajaxSearchAssistant?q=" + urllib2.quote(prefix)
        elif sys.argv[1] == "thefind":
            url = "http://www.thefind.com/search/suggest.js?&q=" + urllib2.quote(prefix)
        outputFile.write(url + "\n")
        # outputFile.write(prefix + "\n")
