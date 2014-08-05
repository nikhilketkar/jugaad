import sys
from collections import defaultdict

class BestsellerRankGroup:
    def __init__(self):
        self.urls = []
        self.pageNumbers = []
        self.positionsOnPage = []
    def add(self, url, pageNo, posOnPage):
        self.urls.append(url)
        self.pageNumbers.append(pageNo)
        self.positionsOnPage.append(posOnPage)
    def computeRanks(self):
        maxProductsOnPage = max(self.positionsOnPage)
        self.ranks = []
        for i in xrange(0,len(self.urls)):
            currRank = ((self.pageNumbers[i] - 1) * maxProductsOnPage) + self.positionsOnPage[i]
            self.ranks.append(currRank)
        return zip(self.urls, self.ranks)

def combineBesellerRankGroups(rankGroups):
    result = []
    for rankGroupName, rankGroupValue in rankGroups.items():
        result.extend(rankGroupValue.computeRanks())
    return sorted(result, key = lambda x: x[1])

categoryToProducts = defaultdict(lambda: defaultdict(BestsellerRankGroup))

with open(sys.argv[1]) as inputFile:
    recordsProcessed = 0
    for line in inputFile:
        PID, MPID, URL, Title, ImageUrl, Category, ScoreFeatures = line.strip().split("\t")
        firstScoreFeature = ScoreFeatures.split(";;")[0]
        pageNumber, positionOnPage, seederPath, crawlTimeStamp = firstScoreFeature.split("||")
        categoryToProducts[Category][seederPath].add(URL,pageNumber,positionOnPage)
        recordsProcessed += 1

with open(sys.argv[2], 'w') as outputFile:
    for category,bestsellerRankGroups in categoryToProducts.items():
        for url, rank in combineBesellerRankGroups(bestsellerRankGroups):
            outputFile.write(category + "\t" + url + "\t" + str(rank) + "\n")
        








  