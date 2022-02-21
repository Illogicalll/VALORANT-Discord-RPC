import aiohttp

async def getParty(accessToken, entitlementsToken, region, playerID):
    session = aiohttp.ClientSession()

    headers = {"X-Riot-Entitlements-JWT": entitlementsToken,
               "Authorization": f'Bearer {accessToken}'}

    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/session/v1/sessions/{playerID}', headers=headers, json={}) as r:
        data = await r.json(content_type='text/plain')
    clientVersion = data['clientVersion']
    
    headers = {"X-Riot-Entitlements-JWT": entitlementsToken,
               "Authorization": f'Bearer {accessToken}',
               "X-Riot-ClientVersion": clientVersion}

    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/parties/v1/players/{playerID}', headers=headers, json={}) as r:
        data = await r.json(content_type='text/plain')
    partyID = data['CurrentPartyID']

    headers = {"X-Riot-Entitlements-JWT": entitlementsToken,
               "Authorization": f'Bearer {accessToken}'}

    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/parties/v1/parties/{partyID}', headers=headers, json={}) as r:
        data = await r.json(content_type='text/plain')
    members = len(data['Members'])
    
    await session.close()
    
    return members