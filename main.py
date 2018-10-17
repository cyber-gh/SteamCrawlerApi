import threading
from queue import Queue
from Spider import Spider
from save_files import *
NUMBER_OF_THREADS = 35

queue = Queue()
Spider()


def create_workers():
    for i in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

def work():
    while True:
        try:
            url = queue.get()
            Spider.crawlPlayer(url,threading.current_thread().name)
            queue.task_done()
        except:
            pass

def create_jobs():
    for link in loadQueue():
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    links = loadQueue()
    if len(links) > 0:
        print(str(len(links)) + ' in the queue')
        create_jobs()

#Spider.crawlPlayer('https://steamcommunity.com/id/Mzeri','1')

create_workers()
create_jobs()