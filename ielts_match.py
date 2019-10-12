import sys
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

MIN_RATE = 35

def loadInto(biglist, filename, prefix):
    f = open(filename, "r")
    contents = f.read().lower()
    currentList = contents.splitlines()
    currentList[:] = [prefix + entry for entry in currentList]
    biglist.extend(currentList)
    
bigList = []
load = lambda fn, p : loadInto(bigList, fn, p)

load("res/p1-1.txt", '1-1:')
load("res/p1-2.txt", '1-2:')
load("res/p1-3.txt", '1-3:')
load("res/p23-1.txt", '23-1:')
load("res/p23-2.txt", '23-2:')
load("res/p23-3.txt", '23-3:')

def omitNum(input):
    return ''.join([i for i in input if (not i.isdigit())])

results = {}

for questionStr in bigList:
    currStr = omitNum(questionStr)
    ratios = process.extract(currStr, bigList, scorer=fuzz.token_set_ratio, limit=8)

    results[questionStr] = []

    for ratio in ratios[1:]:
        results[questionStr] += (ratio,)

outStr = ""

for currQStr in results:
    
    matches = results[currQStr]
    strRepr = ""

    for val in matches:
        name = val[0]
        rate = val[1]
        if rate < MIN_RATE: continue

        strRepr = f"{strRepr}  {val[0]}({str(rate)})\n"

    if len(strRepr) > 0:
        strRepr = f"{currQStr}:\n{strRepr}\n"

    outStr += strRepr


fOut = open('out.txt', "w")
fOut.write(outStr)
fOut.close()

