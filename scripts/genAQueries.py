import sys
import urllib2

for line in sys.stdin:
    searchPhrase = line.strip()
    searchUrl = "http://www.amazon.com/s/&field-keywords=" + urllib2.quote(searchPhrase)
    sys.stdout.write(searchUrl + "\n")


