import sys

error = 0
good = 0

for line in sys.stdin:
    words = line.split('\t')
    if len(words) == 38:
        good += 1
    else:
        error += 1

sys.stderr.write("Good:" + str(good) + "\n")
sys.stderr.write("Error:" + str(error) + "\n")

