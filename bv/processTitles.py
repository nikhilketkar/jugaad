#!/usr/bin/env python

import sys
# import nltk
import re
import string

punctuationRemove = re.compile('[%s]' % re.escape(string.punctuation))
digitsRemove = re.compile('[%s]' % re.escape(string.digits))

def cleanTitle(title):
    text = title.encode("ascii","ignore")
    tokens = text.split()
    # tokens = nltk.word_tokenize(text)
    tokens = [i.encode('string-escape') for i in tokens]
    lowerCaseTokens = [i.lower() for i in tokens]
    punctuationRemoved = [punctuationRemove.sub("", i) for i in lowerCaseTokens]
    digitsRemoved = [digitsRemove.sub("", i) for i in punctuationRemoved]
    emptyRemoved = [i for i in digitsRemoved if len(i) > 0]
    return " ".join(emptyRemoved)

for line in sys.stdin:
    try:
        words = line.split('\t')
        words = [i.strip() for i in words]
        title = words[4]
        words.append(cleanTitle(title))
        sys.stdout.write("\t".join(words) + "\n")
    except:
        pass
