import sys

with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        url, searchText = line.split('\t')
        resultString, breadcrumb = searchText.split(" for ")
        paginationString, resultCount = resultString.split(" of ")
        resultCount = resultCount.replace(",","")
        print breadcrumb, "--------", resultCount