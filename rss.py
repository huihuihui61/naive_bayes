import numpy as np

def calcMostFreq(vocabList,fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.iteritems(),key = operator.itemgetter(1),reverse = True)
    return sortedFreq[:30]

def createVocabList(dataset):
    vocabSet = set([])
    for document in dataset:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def bagOfWords2VecMN(vocabList,inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\W*',bigString)
    vec = []
    for tok in listOfTokens:
        if len(tok) > 2:
            vec.append(tok.lower())
    return vec

def trainNB0(trainMatrix,trainCategory):
    import numpy as np
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    pNoAbsive = 1 - pAbusive
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)
    p0Fenmu = 2.0
    p1Fenmu = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Fenmu += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Fenmu += sum(trainMatrix[i])
    return pAbusive,np.log(p0Num/p0Fenmu),np.log(p1Num/p1Fenmu)

def localWords(feed1,feed0):
    import feedparser
    docList = []
    classList = []
    fullText = []
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30words = calcMostFreq(vocabList,fullText)
    for pairW in top30words:
        if pairW[0] in vocabList:
            vocabList.remove(pairW[0])
    trainingSet = range(2*minLen)
    testingSet = []
    for i in range(20):
        import random
        randIndex = int(random.uniform(0,len(trainingSet)))
        testingSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2VecMN(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    import numpy as np
    p0v,p1v,pSpam = trainNB0(np.array(trainMat),np.array(trainClasses))
    return vocabList,p0v,p1v
    '''
    errorCount = 0
    for docIndex in testingSet:
        wordVector = setOfWord2Vec(vocabList,docList[docIndex])
        print wordVector
        print docList[docIndex]
        print classList[docIndex]
        p0 = sum(p0v * wordVector)
        p1 = sum(p1v * wordVector)
        if p0 > p1:
            print "spam"
        elif p0 < p1:
            print "nspam"
        else:
            print "don't know"
    '''
def setOfWord2Vec(vocabList,inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

if __name__ == "__main__":
    import feedparser
    ny = feedparser.parse("http://newyork.craigslist.org/stp/index.rss")
    sf = feedparser.parse("http://sfbay.craigslist.org/stp/index.rss")
    vocabList, p0v, p1v = localWords(ny,sf)
