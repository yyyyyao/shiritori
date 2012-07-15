import copy
import time
import sys

def checkLink(src, dst):
    dLen = len(dst)
    sLen = len(src)
    if dLen < sLen:
        kLen = dLen
    else:
        kLen = sLen

    while kLen >= 0:
        if src.rfind(dst[:kLen], \
                sLen - kLen, sLen) != -1:
            if kLen == k + 1 or kLen == 0:
                return -1
            else:
                break
        kLen -= 1
    return kLen

def checkState(cList):
    i= 0
    bWord = ""
    ansListNum = []
    kLen = 0
    for word in cList:
        if i != 0:
            ovLap = checkLink(bWord, word)
            if ovLap == -1:
                return []
            ansListNum.append(ovLap)
        bWord = word
        i+=1
    return ansListNum

def printAnswer(aList, aNumList):
    n = 0
    sumIndex = 0
    print ""
    print "Anwser"
    print "-------------"
    bWord = aList.pop(0)
    print bWord
    for word in aList:
        n = aNumList.pop(0)
        sumIndex += len(bWord) - n
        print " " * (sumIndex - 1), word, "  k:", n
        bWord = word

def recurSearch(wIndex, route, fromMap):
    if len(route) == wNum - 1:
        route.append(wIndex)
        return route

    for i in range(wNum):
        if not fromMap[i] and i not in route and i != wIndex:
            return []

    for i in optGMap[wIndex]:
        if i not in route:
            _route = copy.deepcopy(route)
            _route.append(wIndex)
            _fromMap = copy.deepcopy(fromMap)
            for node in _fromMap:
                if wIndex in node:
                    node.remove(wIndex)
            retRoute =  recurSearch(i, _route, _fromMap)
            if retRoute:
                return retRoute
    return []

if __name__ == '__main__':
    k = 3
    wNum = 0 
    argvs = sys.argv
    argc = len(argvs)
    start = time.time()

    if (argc == 2):
        fileName = argvs[1]
    else:
        print "Usage: # python %s filename" % argvs[0]
        print "Use default filename:hoge.txt"
        fileName = "hoge.txt"

    qFp = open(fileName, 'r')
    wList = []
    maxWordLen = 0
    for line in qFp:
        if maxWordLen < len(line):
            maxWordLen = len(line)
        wList.append(line.rstrip())
        wNum += 1
    qFp.close()
    print "Num:", wNum, " ", wList

    gMap = [[0 for j in range(wNum)] for i in range(wNum)]
    optGMap = []
    tGMap = [[0 for j in range(wNum)] for i in range(wNum)]
    optTGMap = []
    for i in range(wNum):
        optGMap.append([])
        optTGMap.append([])

    for i in range(wNum):
        for j in range(wNum):
            if i == j:
                continue
            if checkLink(wList[i], wList[j]) != -1:
                gMap[i][j] = 1
                optGMap[i].append(j)
            if checkLink(wList[j], wList[i]) != -1:
                tGMap[i][j] = 1
                optTGMap[i].append(j)
            
    """
    #for debug.
    print ""
    for i in range(wNum):
        print wList[i].ljust(maxWordLen), gMap[i]
    for i in range(wNum):
        print wList[i].ljust(maxWordLen), tGMap[i]
    print "OptTGmap: fromList"
    for i in range(wNum):
        print wList[i].ljust(maxWordLen), optTGMap[i]
    print "-------------------------------"
    print "OptGmap: toList"
    for i in range(wNum):
        print wList[i].ljust(maxWordLen), optGMap[i]

    #number of dst words.
    toList = []
    for i in range(wNum):
        pathNum = gMap[i].count(1)
        toList.append((i, pathNum))
    toList.sort(cmp=lambda x, y: x[1] - y[1])
    """

    #number of src words.
    fromList = []
    for i in range(wNum):
        pathNum = tGMap[i].count(1)
        fromList.append((i, pathNum))
    fromList.sort(cmp = lambda x, y: x[1] - y[1])

    for dat in fromList:
        i = dat[0]
        print "start", i
        route = []
        ansRoute = recurSearch(i, route, optTGMap)
        if ansRoute:
            break

    end = time.time()
    print "Time:", end - start

    ansWList = []
    for i in ansRoute:
        ansWList.append(wList[i])

    ansList = checkState(ansWList)
    if ansList:
        printAnswer(ansWList, ansList)
    else:
        "No Answer"
