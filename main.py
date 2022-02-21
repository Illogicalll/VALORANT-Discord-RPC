from auth import userAuth
from party import getParty
import asyncio

auth = asyncio.get_event_loop().run_until_complete(userAuth(input('Enter Username: '),input('Enter Password: ')))
accessToken, entitlementsToken, playerID = auth[0], auth[1], auth[2]

region = input('Enter Region (na/eu/ap/kr): ')
choices = ['na','eu','ap','kr']
valid = False
while valid == False:
    if region in choices:
        valid = True
    else:
        region = input('Invalid Region, Please Re-Enter (na/eu/ap/kr): ')

members = asyncio.get_event_loop().run_until_complete(getParty(accessToken, entitlementsToken, region, playerID))
print(f'In Party: {members} of 5')

input('Press Enter To Exit...')