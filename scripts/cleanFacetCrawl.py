import sys

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

sys.stdout.write("STATUS\tAMAZON_TITLE\tAMAZON_MARKETPLACE_TITLE\tAMAZON_URL\tAMAZON_MARKETPLACE_URL\tDRUGSTORE_URL\tFACETS\n")
for line in sys.stdin:
    try:
        if line.startswith("SUCCESS"):
            STATUS, AMAZON_TITLE, AMAZON_MARKETPLACE_TITLE, AMAZON_URL, AMAZON_MARKETPLACE_URL, DRUGSTORE_URL, FACETS = line.split('\t')
            baseFacetList = [i.strip() for i in FACETS.split('|')]
            actualFacetList = [] 
            start = False
            for i in baseFacetList:
                if i == "& Up":
                    break
                if hasNumbers(i):
                    break
                if i == "Free Shipping by Amazon" or i == "Subscribe & Save Eligible" or i == "AmazonGlobal Eligible":
                    start = True
                if start:
                    if i != "Free Shipping by Amazon" and i != "Subscribe & Save Eligible" and i != "AmazonGlobal Eligible":
                        if len(i) > 0:
                            actualFacetList.append(i)
            if len(actualFacetList) > 0:
                facets = "|".join(actualFacetList)
                fragments = ["TAGS_FOUND"] + line.split('\t')[1:-1] + [facets]
                sys.stdout.write("\t".join(fragments) + "\n")        
            else:
                fragments = ["TAGS_NOT_FOUND"] + line.split('\t')[1:-1] + ["NA"]
                sys.stdout.write("\t".join(fragments) + "\n")        
        else:
            fragments = ["TAGS_NOT_FOUND"] + line.split('\t')[1:-1] + ["NA"]
            sys.stdout.write("\t".join(fragments) + "\n")        
    except:
        fragments = ["TAGS_NOT_FOUND"] + line.split('\t')[1:-1] + ["NA"]
        sys.stdout.write("\t".join(fragments) + "\n")        
