#coding:utf-8
import numpy as np
import math
def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                 ['maybe','not','take','him','to','dog','park','stupid'],
                 ['my','dalmation','is','so','cute','I','love','him'],
                 ['stop','posting','stupid','worthless','garbage'],
                 ['mr','licks','ate','my','steak','how','to','stop','him'],
                 ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1]
    return postingList,classVec

def createVocabList(dataset):
    vocabSet = set([])
    for document in dataset:
        vocabSet = vocabSet | set(document)  # 创建两个集合的并集
    # 此时vocabSet具有全部出现的单词，且只有一个
    return list(vocabSet)

def setOfWord2Vec(vocabList,inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    pNoAbsive = 1 - pAbusive
    p0Num = np.ones(numWords)
    p1Num = np.ones(numWords)
    p0Fenmu = 2.0
    p1Fenmu = 2.0
    for i in range(numTrainDocs):   #遍历每一篇doc
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Fenmu += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Fenmu += sum(trainMatrix[i])
    return pAbusive,np.log(p0Num/p0Fenmu),np.log(p1Num/p1Fenmu)

if __name__ == "__main__":
    dataset, label = loadDataSet()
    vocList = createVocabList(dataset)
    print vocList
    a = list()
    for item in dataset:
        vec = setOfWord2Vec(vocList, item)
        a.append(vec)
    dataTrain = np.array(a)
    pAbusive, p0Vec, p1Vec = trainNB0(dataTrain, label)
    print pAbusive
    print p0Vec
    print p1Vec

    test = ["I","am","clever"]
    vec = setOfWord2Vec(vocList,test)
    print vec
    p_0 = sum(p0Vec * vec)
    p_1 = sum(p1Vec * vec)
    print p_0
    print p_1
    if p_1 > p_0:
        print "abusive"
    elif p_1 < p_0:
        print "not abusive"
    else:
        print "equal"