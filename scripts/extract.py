import sys
import lxml.html

def clean(text):
    return ''.join(i for i in text if ord(i)<128)

with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        words = line.split('\t')
        if words[0] == "SUCCESS":
            with open(words[2].strip()) as currFile:
                try:
                    data = currFile.read()
                    root = lxml.html.fromstring(data)
                    breadCrumb = "".join([i.strip() for i in root.cssselect('#s-result-count')[0].itertext()][1:]).replace(":", " > ")
                    titles = [i.text for i in root.cssselect('.lrg.bold')]
                    for title in titles:
                        sys.stdout.write(clean(breadCrumb) + "\t" + clean(title) + "\n")
                except:
                    pass
