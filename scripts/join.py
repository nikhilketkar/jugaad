import sys

url2category = {}
with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        words = line.split('\t')
        url = words[0]
        category = [4]
        url2category[url] = category

url2category = {}
with open(sys.argv[2]) as inputFile:
    with open(sys.argv[3], 'w') as outputFile:
        for line in inputFile:
            words = line.split('\t')
            url = words[2]
            outputFile.write(line.strip() + "\t" + url2category[url] + "\n")