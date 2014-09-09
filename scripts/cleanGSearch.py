import sys
import lxml.html

def getSearchString(root):
    return root.cssselect('#sbhost')[0].attrib["value"]

def getURLs(root):
    return [i.getchildren()[0].attrib["href"] for i in root.cssselect('.r')]

for line in sys.stdin:
    try:
        filename = line.strip()
        with open(filename) as inputFile:
            data = inputFile.read()
        root = lxml.html.fromstring(data)
        searchString = getSearchString(root)
        urls = getURLs(root)
        for url in urls:
            sys.stdout.write("SUCCESS" + "\t" + filename  + "\t" + searchString + "\t" + url + "\n")
    except:
            sys.stdout.write("FALIURE" + "\t" + filename  + "\n")
        
