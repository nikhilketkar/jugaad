import sys

with open(sys.argv[1]) as inputFile:
    recordsProcessed = 0
    for line in inputFile:
        PID, MPID, URL, Title, Category, ImageUrl, ScoreFeatures = line.strip().split("\t")
        firstScoreFeature = ScoreFeatures.split(";;")[0]
        pageNumber, positionOnPage, seederPath, crawlTimeStamp = firstScoreFeature.split("||")
        recordsProcessed += 1
    sys.stderr.write(str(recordsProcessed) + " records parsed successfully.\n" )

        