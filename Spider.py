from Player import Player
import time
from ApiRequests import *
from save_files import *


class Spider(object):
    queue_file = 'queue.txt'
    visited_file = 'visited.txt'
    results_file = 'results.txt'
    queue = set()
    visited = set()
    results = set()
    MAX_QUEUE_LEN = 10000000
    max = 210 - 137

    def loadFiles():
        Spider.queue = loadQueue(Spider.queue_file)
        Spider.visited = loadVisited(Spider.visited_file)

    def __init__(self):
        Spider.loadFiles()
        super().__init__()

    def evaluatePlayer(steamlink):
        steamlink = steamLinkToId(steamlink)
        if not getPlayerStatus(steamlink):
            return Player(steamlink,0,0,0)
        lvl = getUserLevel(steamlink)
        hours = getHours(steamlink)
        money = getInventoryValue(steamlink)
        return Player(IdToSteamLink(steamlink),money,hours,lvl)

    def saveFiles():
        saveQueue(Spider.queue)
        saveVisited(Spider.visited)
        #saveResults(Spider.results)  


    def crawlPlayer(steamlink,threadname):
        print('Queue len = ' + str(len(Spider.queue)))
        Spider.queue.remove(steamlink)
        if steamlink in Spider.visited:
            Spider.updateFiles()
            return 
        else:
            Spider.visited.add(steamlink)
        #print(threadname + ' crawling ' + steamLinkToId(steamlink))
        P = Spider.evaluatePlayer(steamlink)
        appendScanned(P)
        P.show()
        if (P.isGood()):
            print('-----------------------------------')
            #print(threadname + ' caught this one')
            #P.show()
            print('Number of players caught = ' + str(len(Spider.results)))
            #print('-----------------------------------')
            Spider.results.add(P)
            appendResult(P)
            
            if len(Spider.queue) <= Spider.MAX_QUEUE_LEN:
                Spider.queue.update(getFriends(steamlink))
        Spider.saveFiles()