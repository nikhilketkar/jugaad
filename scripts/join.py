import sys


url2category = {}
with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        words = line.split('\t')
        url = words[0].strip()
        category = words[4].strip()
        url2category[url] = category

with open(sys.argv[2]) as inputFile:
    with open(sys.argv[3], 'w') as outputFile:
        for line in inputFile:
            words = line.split('\t')
            url = words[2].strip()
            outputFile.write(line.strip() + "\t" + url2category[url] + "\n")