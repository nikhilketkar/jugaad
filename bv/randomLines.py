import sys
import random

random.seed(sys.argv[1])
sampleSize = int(sys.argv[2])
inputFilename = sys.argv[3]
outputFilename = sys.argv[4]

with open(inputFilename) as inputFile:
    lines = inputFile.readlines()

with open(outputFilename, 'w') as outputFile:
    for i in xrange(0, sampleSize):
        randomPosition = random.randint(0, len(lines))
        outputFile.write(lines[randomPosition])

