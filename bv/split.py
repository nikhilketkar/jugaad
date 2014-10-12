import sys

with open(sys.argv[1], 'w') as sourceRecords:
    with open(sys.argv[2], 'w') as destinationRecords:
        for line in sys.stdin:
            words = line.split('\t')
            if words[1] == "Both":
                sourceRecords.write(line)                
                destinationRecords.write(line)
            elif words[1] == "Source":
                sourceRecords.write(line)
            else:
                destinationRecords.write(line)
