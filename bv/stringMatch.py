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
    def lookup1(self, column):
        return self.mapper[column]
    def lookup2(self, column):
        return self.columnCount + self.mapper[column] 


punctuationRemove = re.compile('[%s]' % re.escape(string.punctuation))
digitsRemove = re.compile('[%s]' % re.escape(string.digits))

def cleanTitle(title):
    tokens = title.split()
    tokens = [i.encode('string-escape') for i in tokens]
    lowerCaseTokens = [i.lower() for i in tokens]
    punctuationRemoved = [punctuationRemove.sub("", i) for i in lowerCaseTokens]
    digitsRemoved = [digitsRemove.sub("", i) for i in punctuationRemoved]
    emptyRemoved = [i for i in digitsRemoved if len(i) > 0]
    return set(emptyRemoved)

cm = ColumnMapper()
for line in sys.stdin:
    try:
        words = line.split('\t')
        words = [i.strip() for i in words]
        title1 = cleanTitle(words[cm.lookup1("ProductName")])
        title2 = cleanTitle(words[cm.lookup2("ProductName")])
        score = len(title1.intersection(title2))
        if score > 0:
            sys.stdout.write(str(score) + "\t" + line)
    except Exception as e:
        logging.exception(e)
