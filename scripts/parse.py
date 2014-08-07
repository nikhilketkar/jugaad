import sys

import lxml.html

with open(sys.argv[1]) as logFile:
    with open(sys.argv[2],'w') as outputFile:
        for line in logFile:
            try:
                words = line.strip().split('\t')
                status = words[0]
                url = words[1]
                path = words[2]
                with open(path) as htmlFile: htmlData = htmlFile.read()
                root = lxml.html.fromstring(htmlData)
                if status == "SUCCESS":
                    try:
                        text = " ".join([j.strip() for j in root.cssselect("#s-result-count")[0].itertext()])
                    except:
                        text = " ".join([j.strip() for j in root.cssselect("#noResultsTitle")[0].itertext()])
                    outputFile.write(url + "\t" + text + "\n")                
            except Exception as e:
                sys.stderr.write("ERROR " + str(e) + "\t" + line)
