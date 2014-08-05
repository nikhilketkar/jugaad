import sys
from collections import defaultdict
import numpy
from scipy import stats

contextToCategory = defaultdict(list)

with open(sys.argv[1]) as inputFile:
    recordsProcessed = 0
    for line in inputFile:
        PID, MPID, URL, Title, Category, ImageUrl, ScoreFeatures = line.strip().split("\t")
        firstScoreFeature = ScoreFeatures.split(";;")[0]
        pageNumber, positionOnPage, seederPath, crawlTimeStamp = firstScoreFeature.split("||")
        contextToCategory[seederPath].append(Category)
        recordsProcessed += 1
    sys.stderr.write(str(recordsProcessed) + " records processed successfully.\n" )

with open(sys.argv[2], 'w') as outputFile:
    for key, value in contextToCategory.items():
        total = float(len(value))
        commonValue, commonCount = stats(numpy.array(value))
        outputFile.write(str(commonCount[0]/total) + "\t" + commonValue[0] + "\t" + key + "\n")