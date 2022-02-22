from auth import userAuth
from party import getParty
from session import getSession
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
while run == True:
    if looped == 0 or looped == 660:
        auth = asyncio.get_event_loop().run_until_complete(userAuth(username,password))
        accessToken, entitlementsToken, playerID = auth[0], auth[1], auth[2]
        looped = 0

    members = asyncio.get_event_loop().run_until_complete(getParty(accessToken, entitlementsToken, region, playerID))
    print(f'In Party: {members} of 5')

    session = asyncio.get_event_loop().run_until_complete(getSession(accessToken, entitlementsToken, region, playerID))
    if len(session[1]) > 0 and len(session[2]) > 0 and len(str(session[3])) > 0 and len(str(session[4])) > 0:
        print(f'Currently {session[0]}: {session[1]} ({session[2]}) | {session[3]} - {session[4]}')
    elif len(session[1]) > 0:
        print(f'Currently {session[0]}: {session[1]}')
    else:
        print(f'Currently {session[0]}')
    time.sleep(5)
    looped += 1

input('Press Enter To Exit...')