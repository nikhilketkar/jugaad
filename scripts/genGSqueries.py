import sys
import urllib2

def genQuery(query):
    return "https://www.google.com/search?&tbm=shop&q=" + urllib2.quite(query)

for line in sys.stdin:
    sys.stdout.write(genQuery(line.strip()))

