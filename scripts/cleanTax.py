import sys

with open("/Users/nikhil/Desktop/CategoryTree_Semantics3.txt") as inputFile:
    currList = []
    for line in inputFile:
        identifier, rest = line.strip().split('.', 1)
        breadcrumb = "(".join(rest.split('(')[:-1]).strip()
        identifier = int(identifier)
        if len(currList) < identifier:
            currList.append(breadcrumb)
        else:
            while(len(currList) >= identifier):
                currList.pop()
            currList.append(breadcrumb)            
        sys.stdout.write("\t".join(currList) + "\n")