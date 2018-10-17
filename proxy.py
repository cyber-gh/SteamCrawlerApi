import asyncio
from proxybroker import Broker
from tqdm import tqdm

async def save(proxies, filename):
    """Save proxies to a file."""
    with open(filename, 'a') as f:
        while True:
            proxy = await proxies.get()
            if proxy is None:
                break
            proto = 'https' if 'HTTPS' in proxy.types else 'http'
            row = '%s %s:%d\n' % (proto, proxy.host, proxy.port)
            f.write(row)


def getProxies(type, nr):
    proxies = asyncio.Queue()
    broker = Broker(proxies)
    tasks = asyncio.gather(broker.find(types=[ type], limit=nr),
                           save(proxies, filename='proxies.txt'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(tasks)

def loadProxies():
    print('Loading proxies...')
    #getProxies('HTTP',400)
    print('HTTP proxies loaded')
    #getProxies('HTTPS',10)

    fw = open('proxies.txt','r')
    content = fw.readlines()
    content = [x.strip() for x in content]
    d = dict()
    http = list()
    https = list()
    for el in content:
        tmp = el.split(' ')
        if (tmp[0] == 'http'):
            http.append(tmp[1])
        else:
            https.append(tmp[1])
        #d.update({tmp[0]:tmp[1]})
    print('Proxies loaded succesfully')
    return http,https






