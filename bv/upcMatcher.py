#!/usr/bin/env python

import sys
import re
import string

upcPosition = 11

def loadFile(filename):
    ib = {}
    with open(filename) as inputFile:
        for line in inputFile:
            try:
                words = line.split('\t')
                upc = words[upcPosition].strip()
                ib[upc] = line
            except:
                pass
    return ib

ib = loadFile("source.tsv")
for line in sys.stdin:
    try:
        words = line.split('\t')
        words = [i.strip() for i in words]
        upc = words[upcPosition].strip()
        if upc != "NA":
            if upc in ib:
                sys.stdout.write(ib[upc].strip() + line)
    except:
        pass

