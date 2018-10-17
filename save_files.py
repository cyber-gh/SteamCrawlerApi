import os

QueueFile = 'queue.txt'
VisitedFile = 'visited.txt'
ResultsFile = 'results.txt'
ScannedFile = 'scanned.txt'


def loadQueue(file_name = QueueFile):
    fq = open(file_name,'r')
    content = fq.readlines()
    content = [x.strip() for x in content]
    content = [x.split(" ")[0] for x in content]
    Queue = set(content)
    return Queue

def loadVisited(file_name = VisitedFile):
    fq = open(file_name,'r')
    content = fq.readlines()
    content = [x.strip() for x in content]
    Queue = set(content)
    return Queue

def saveQueue(Queue):
    copyQueue = set(Queue)
    fq = open(QueueFile,'w')
    for el in copyQueue:
        fq.write(el)
        fq.write('\n')


def saveVisited(Queue):
    copyQueue = set(Queue)
    fq = open(VisitedFile,'w')
    for el in copyQueue:
        fq.write(el)
        fq.write('\n')


def saveResults(EvaluatedPlayers):
    fr = open(ResultsFile,'w')
    for el in EvaluatedPlayers:
        fr.write(el.steamlink + ' '+ str(el.inventoryValue) + ' ' + str(el.hours) + ' ' + str(el.level) + '\n')

def appendScanned(Player):
    fr = open(ScannedFile,'a')
    el = Player
    fr.write(el.steamlink + ' '+ str(el.inventoryValue) + ' ' + str(el.hours) + ' ' + str(el.level) + '\n')

def appendResult(Player):
    fr = open(ResultsFile,'a')
    el = Player
    fr.write(el.steamlink + ' '+ str(el.inventoryValue) + ' ' + str(el.hours) + ' ' + str(el.level) + '\n')

def threadName(k):
    return 'Thread-'+str(k)
