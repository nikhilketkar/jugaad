import sys
import json

def removeUnicode(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

try:
    with open(sys.argv[1]) as inputFile: data = inputFile.read()
    jdata = json.loads(data)
    queries = jdata["data"]["qpm"]
    for query in queries:
        sys.stdout.write(removeUnicode(query) + "\n")
except:
    sys.stderr.write("ERROR " + sys.argv[1] + "\n")
