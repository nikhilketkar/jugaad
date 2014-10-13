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

cm = ColumnMapper()
for line in sys.stdin:
    try:
        words = line.split('\t')
        words = [i.strip() for i in words]
        destination = words[:19]
        source = words[19:]
        destinationUPC = destination[cm.lookup("UPC")]
        sourceUPC = source[cm.lookup("UPC")]
        if sourceUPC == destinationUPC and sourceUPC != "NA" and sourceUPC != "000000000000":
            sys.stdout.write(line)
    except Exception as e:
        logging.exception(e)
