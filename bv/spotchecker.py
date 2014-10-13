import sys
import os

correct = 0.0
incorrect = 0.0

with open(sys.argv[1]) as inputFile:
    records = inputFile.readlines()

for line in records:
    os.system('clear')
    sys.stdout.write(line)
    result = raw_input('Enter your input:')
    if result == 'n':
        incorrect += 1
    else:
        correct += 1
sys.stdout.write("Accuracy:" + str(correct/(correct + incorrect)))
