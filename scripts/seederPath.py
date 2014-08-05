import sys

seederPaths = set([])

with open(sys.argv[1]) as inputFile:
    recordsProcessed = 0
    for line in inputFile:
        PID, MPID, URL, Title, ImageUrl, Category, ScoreFeatures = line.strip().split("\t")
        firstScoreFeature = ScoreFeatures.split(";;")[0]
        pageNumber, positionOnPage, seederPath, crawlTimeStamp = firstScoreFeature.split("||")
        seederPaths.add(seederPath)
        recordsProcessed += 1
    sys.stderr.write(str(recordsProcessed) + " records processed successfully.\n" )

with open(sys.argv[2], 'w') as outputFile:
    for seeederPath in seederPaths:
        outputFile.write(seederPath + "\n")