#!/usr/bin/env python

import sys
import re
import string
import logging

#ClientName,Sku,ProductName,BrandName,CategoryName,Inactive,Description,ProductPageURL,ImageURL,UPC,EAN,GTIN,ModelNumber,ManufacturerPartNumber,ISBN,Price,ReviewPageTitle

class ColumnMapper:
    def __init__(self):
        columns = ["File","RecordType","ClientName","Sku","ProductName","BrandName","CategoryName","Inactive",\
                   "Description","ProductPageURL","ImageURL","UPC","EAN","GTIN","ModelNumber","ManufacturerPartNumber","ISBN","Price","ReviewPageTitle"]
        self.mapper = {}
        for column, position in zip(columns,range(0, len(columns))):
            self.mapper[column] = position
    def lookup(self, column):
        return self.mapper[column]

class CodeMatcher:
    def __init__(self, position):
        self.ib = {}
        self.position = position
    def insert(self, record):
        code = record[self.position].strip()
        if code != "NA":
            self.ib[code] = record
    def lookup(self, record):
        code = record[self.position].strip()
        if code != "NA" :
            if code in self.ib:
                return self.ib[code]
            else:
                return False
        return False

def loadFile(filename):
    columnMapper = ColumnMapper()
    codeMatchers = [CodeMatcher(columnMapper.lookup("Sku")),\
                    CodeMatcher(columnMapper.lookup("UPC")),\
                    CodeMatcher(columnMapper.lookup("EAN")),\
                    CodeMatcher(columnMapper.lookup("GTIN")),\
                    CodeMatcher(columnMapper.lookup("ModelNumber")),\
                    CodeMatcher(columnMapper.lookup("ManufacturerPartNumber")),\
                    CodeMatcher(columnMapper.lookup("ISBN"))]
    with open(filename) as inputFile:
        for line in inputFile:
            try:
                words = line.split('\t')
                words = [i.strip() for i in words]
                for codeMatcher in codeMatchers:
                    codeMatcher.insert(words)
            except:
                pass
    return codeMatchers

codeMatchers = loadFile("sourceRecords.tsv")
for line in sys.stdin:
    try:
        words = line.split('\t')
        words = [i.strip() for i in words]
        matchResult = [codeMatcher.lookup(words) for codeMatcher in codeMatchers]
        if any(matchResult):
            for match in matchResult:
                if match:
                    sys.stdout.write("\t".join(words + match) + "\n")
    except Exception as e:
        logging.exception(e)

