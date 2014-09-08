import sys
import urllib2

def genQuery(query):
    return "https://www.google.com/search?&tbm=shop&q=" + urllib2.quote(query)

for line in sys.stdin:
    sys.stdout.write(genQuery(line.strip()))

