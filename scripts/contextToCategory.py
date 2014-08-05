import sys

with open(sys.argv[1]) as inputFile:
    for line in inputFile:
        PID, MPID, URL, Title, Category, ImageUrl, ScoreFeatures = line.strip().split("\t")
        firstScoreFeature = ScoreFeatures.split(";;")[0]
        pageNumber, positionOnPage, seederPath, crawlTimeStamp = firstScoreFeature.split("||")
        