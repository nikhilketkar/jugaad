import sys
import lxml.html

for line in sys.stdin:
    if line.startswith("SUCCESS"):
        STATUS, AMAZON_URL, FILENAME = line.strip().split('\t')
        with open(FILENAME) as inputFile:
            data = inputFile.read()
        root = lxml.html.fromstring(data)
        refinementURLs = ["http://www.amazon.com" + i.getparent().attrib['href'] for i in root.cssselect('.childRefinementLink')]
        if len(refinementURLs) < 1:
            refinementURLs = ["http://www.amazon.com" + i.getparent().attrib['href'] for i in root.cssselect('.boldRefinementLink')]
        if len(leafUrls) > 0:
            for refinementURL in refinementURLs:
                sys.stdout.write("SUCCESS" + "\t" + AMAZON_URL + "\t" + refinementURL + "\n")
        else:
            sys.stdout.write("FAILURE" + "\t" + AMAZON_URL + "\n")

        
        
