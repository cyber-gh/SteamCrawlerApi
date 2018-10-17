import requests
import json
import xml.etree.ElementTree as ET
import urllib3, re
from xml.dom import minidom
import time
from proxy import *
import random
import cfscrape
STEAM_WEB_API_KEY = 'EE8C39A0DBE155B42883B3E37CBF0856'
STEAMID_API_KEY = '5QHEFLFES45VW48788CN'

http,https = loadProxies()


def checkNick(nick):
    letter = re.findall(r'[\u4e00-\u9fff]+', nick)
    if len(letter) > 0:
        return False
    return True
        


def requestResponse(link,useProxies ):
    Tries = 0
    scraper = cfscrape.create_scraper()
    while True:
        try:
            if Tries >= 1:
                useProxies = True
            Tries +=1
            proxies = {
                 'http': 'http://' + http[random.randint(0,len(http)-1)],
                 'https': 'https://' + https[random.randint(0,len(https)-1)],
                }
            if useProxies:
                response = scraper.get(link, proxies=proxies)
            else:
                response = scraper.get(link)
            break
        except:
            print('connection error, trying again...')
            print(link)
            continue
    return response

def getUserLevel(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = str('http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?')
    requestLink += str('key=' + str(key))
    requestLink += str('&steamid=' + str(steamid))
    response = requestResponse(requestLink,False)
    level = json.loads(response.content.decode('utf-8'))['response']
    return level['player_level']
#deprecated method
def getHoursPlayed(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = str('http://steamcommunity.com/profiles/')
    requestLink += str(steamid + '/stats/csgo/?xml=1')
    response = requestResponse(requestLink,False)
    root = ET.fromstring(response.content)
    for child in root.iter('hoursPlayed'):
        return float(child.text)

def getTimePlayed(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = str(' http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730')
    requestLink += str('&key=' + str(key))
    requestLink += str('&steamid=' + str(steamid))
    response = requestResponse(requestLink,False)
    data = json.loads(response.content.decode('utf-8'))['playerstats']['stats']
    #with open('test.txt','w') as f:
    #    json.dump(data,f)
    matches_played = [item for item in data if item['name'] == 'total_matches_played'][0]['value']
    return float(matches_played)*45/60

def convertToSteamID(customurl):
    key = STEAMID_API_KEY
    customurl.lower()
    requestLink = 'https://steamid.eu/api/request.php?'
    requestLink += str('api=' + str(key) + '&player=' + customurl + '&request_type=5&format=json')
    response = requestResponse(requestLink,False)
    data = json.loads(response.content.decode('utf-8'))
    #with open('test.txt','w') as f:
    #    json.dump(data,f)
    try:
        rs = data['linked_users']['steamid64']
    except:
        print('error converting player')
        rs = '76561198158383654'
    return (rs)

def getInventoryValue(steamid):
    requestLink = 'http://185.25.148.26/api/GetInventoryValue/?'
    requestLink += str('id=' + steamid)
    while True:
        response = requestResponse(requestLink,True)
        data = json.loads(response.content.decode('utf-8'))
        #data = dict(data)
        if data['success'] == "exceeded maximum number of requests, try again in next hour":
            print('Too manyt tries on this proxy')
            continue 
        if data['success'] == 'false':
            return 0
        return float(data['value'])

def isBanned(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = 'http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?'
    requestLink += str('key=' + key + '&steamids=' + steamid)
    response = requestResponse(requestLink,False)
    data = json.loads(response.content.decode('utf-8'))
    #with open('test.txt','a') as f:
    #    json.dump(data,f)
    return bool(data['players'][0]['VACBanned'])

def getHours(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?'
    requestLink += str('key=' + key + '&steamid=' + steamid)
    response = requestResponse(requestLink,False)
    data = json.loads(response.content.decode('utf-8'))
    try:
        data = data['response']
        if data['game_count'] >50:
            return 100000
        data = data['games']
        rs = 0
        playtime = [item['playtime_forever'] for item in data if item['appid'] == 730]
        if (len(playtime)) == 0:
            return 0
        rs = playtime[0]/60
        return rs
    except:
        return 0


def getFriendsList(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?'
    requestLink += str('key=' + key + '&steamid=' + steamid)
    response = requestResponse(requestLink,False)
    data = json.loads(response.content.decode('utf-8'))
    data = data['friendslist']['friends']
    data = [id['steamid'] for id in data ]
    return data

def getPlayerStatus(steamid):
    key = STEAM_WEB_API_KEY
    requestLink = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?'
    requestLink += str('key=' + key + '&steamids=' + steamid)
    response = requestResponse(requestLink,False)
    data = json.loads(response.content.decode('utf-8'))
    data = data['response']['players'][0]
    rs = list()
    nick = data['personaname']
    #if not checkNick(str(nick)):
    #    return False
    
    if "loccountrycode" in data and data["loccountrycode"] == 'CN':
        return False
    if int(data['profilestate']) == 1:
        rs.append(True)
    else:
        rs.append(True)

    lastlog = (int(time.time()) - data['lastlogoff']) / 3600
    if (lastlog > 30):
        rs.append(False)
    else:
        rs.append(True)
    return rs[0] and rs[1] and (not isBanned(steamid))

def steamLinkToId(steamlink):
    if steamlink[-1] == '/':
        steamlink = steamlink[:-1]
    steamlink = steamlink.split('/')
    if steamlink[-2] == 'id':
        return convertToSteamID(steamlink[-1])
    else:
        return steamlink[-1]

def IdToSteamLink(steamid):
    return 'https://steamcommunity.com/profiles/' + steamid

def getFriends(steamlink):
    steamlink = steamLinkToId(steamlink)
    Friends = getFriendsList(steamlink)
    Results = set()
    for el in Friends:
        Results.add(IdToSteamLink(el))
    return (Results)

#print(getInventoryValue('76561198178007945'))
#print(getInventoryValue('76561198191288519'))
#print(getPlayerStatus('https://steamcommunity.com/profiles/76561198374623321'))

#proxies = {
#                 'http': 'http://' + http[random.randint(0,len(http)-1)],
#                 'https': 'https://' + https[random.randint(0,len(https)-1)],
#                }

#response = requests.get('http://www.google.com?',proxies=proxies)

#getFriends('https://steamcommunity.com/profiles/76561198365010891')
#print(steamLinkToId('https://steamcommunity.com/id/joy28/'))
#print(getFriendsList(STEAM_WEB_API_'76561198060033735'))
#print(getInventoryValue('76561198158383654'))
#print(getPlayerStatus(STEAM_WEB_API_'76561198158383654'))






