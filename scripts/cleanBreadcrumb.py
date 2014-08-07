import sys

with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        print line.strip()
        url, searchText = line.strip().split('\t')
        resultString, breadcrumb = searchText.split(" for ")
        try:
            paginationString, resultCount = resultString.split(" of ")
        except:
            resultCount = resultString
        resultCount = resultCount.replace(",","").replace("results", "")
        print breadcrumb, "--------", resultCount