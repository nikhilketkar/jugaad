import sys
import re
import string
import logging



class ColumnMapper:
    def __init__(self):
        columns = ["File","RecordType","ClientName","Sku","ProductName","BrandName","CategoryName","Inactive",\
                   "Description","ProductPageURL","ImageURL","UPC","EAN","GTIN","ModelNumber","ManufacturerPartNumber","ISBN","Price","ReviewPageTitle"]
        self.columnCount = len(columns)
        self.mapper = {}
        for column, position in zip(columns,range(0, self.columnCount)):
            self.mapper[column] = position
    def lookup(self, column):
        return self.mapper[column]

punctuationRemove = re.compile('[%s]' % re.escape(string.punctuation))
digitsRemove = re.compile('[%s]' % re.escape(string.digits))

def cleanTitle(title):
    tokens = title.split()
    tokens = [i.encode('string-escape') for i in tokens]
    lowerCaseTokens = [i.lower() for i in tokens]
    # punctuationRemoved = [punctuationRemove.sub("", i) for i in lowerCaseTokens]
    # digitsRemoved = [digitsRemove.sub("", i) for i in punctuationRemoved]
    NARemoved = [i for i in lowerCaseTokens if i != "NA"] 
    emptyRemoved = [i for i in NARemoved if len(i) > 0]
    return set(emptyRemoved)

cm = ColumnMapper()
for line in sys.stdin:
    try:
        words = line.split('\t')
        words = [i.strip() for i in words]
        destination = words[:19]
        source = words[19:]
        destinationTitle = cleanTitle(destination[cm.lookup("ProductName")])
        sourceTitle = cleanTitle(source[cm.lookup("ProductName")])
        score = len(sourceTitle.intersection(destinationTitle))
        if score > 0:
            sys.stdout.write(line)
    except Exception as e:
        logging.exception(e)
