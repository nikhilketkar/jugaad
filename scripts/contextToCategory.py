import sys
from collections import defaultdict, Counter

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
        counter = Counter(value)
        total = float(sum(counter.values()))
        category, count = counter.most_common(1)[0]
        outputFile.write(str(count/total) + "\t" + category + "\t" + key + "\n")