from auth import userAuth
from party import getParty
from session import getSession
from discordpres import updateRPC
from discordpres import startRPC
import asyncio
import time

username = input('Enter Username: ')
password = input('Enter Password: ')
region = input('Enter Region (na/eu/ap/kr): ')
choices = ['na','eu','ap','kr']
valid = False
while valid == False:
    if region in choices:
        valid = True
    else:
        region = input('Invalid Region, Please Re-Enter (na/eu/ap/kr): ')

run = True
looped = 0
prev = 0
displayedScore = []
actualScore = []
startRPC()
while run == True:
    if looped == 0 or looped == 660:
        auth = asyncio.get_event_loop().run_until_complete(userAuth(username,password))
        accessToken, entitlementsToken, playerID = auth[0], auth[1], auth[2]
        looped = 0

    members = asyncio.get_event_loop().run_until_complete(getParty(accessToken, entitlementsToken, region, playerID))
    session = asyncio.get_event_loop().run_until_complete(getSession(accessToken, entitlementsToken, region, playerID))
    actualScore = [session[3], session[4]]

    if len(session[1]) > 0 and len(session[2]) > 0 and len(str(session[3])) > 0 and len(str(session[4])) > 0 and displayedScore != actualScore:
        prev = 1
        displayedScore = [session[3],session[4]]
        updateRPC(1, session[0], members, session[1], session[3], session[4], session[2])
    elif len(session[1]) > 0 and prev != 2 and len(str(session[3])) == 0:
        prev = 2
        updateRPC(2, session[0], members, session[1], session[3], session[4], session[2])
    elif session[0] == 'In Menus' and prev != 3:
        prev = 3
        updateRPC(3, session[0], members, session[1], session[3], session[4], session[2])

    time.sleep(1)
    looped += 1

input('Press Enter To Exit...')