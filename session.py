import aiohttp
from valclient.client import Client

async def getSession(accessToken, entitlementsToken, region, playerID):
    session = aiohttp.ClientSession()

    headers = {"X-Riot-Entitlements-JWT": entitlementsToken,
               "Authorization": f'Bearer {accessToken}'}

    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/session/v1/sessions/{playerID}', headers=headers, json={}) as r:
        data = await r.json(content_type='text/plain')
    gamefilesState = data['loopState'].lower().capitalize()
    stateTranslate = {'Ingame':'In-Game', 'Menus':'In Menus', 'Pregame':'In Pre-Game'}
    state = stateTranslate[gamefilesState]

    gamemodeTranslate = {'spikerush':'Spike Rush', 'deathmatch':'Deathmatch', 'onefa':'Replication', 
                         'unrated':'Unrated', 'competitive': 'Competitive', 'ggteam': 'Escalation',
                         'snowball': 'Snowball Fight'}
    mapTranslations = {'Port':'Icebox', 'Ascent':'Ascent', 'Canyon':'Fracture', 'Duality':'Bind', 
                       'Triad': 'Haven', 'Bonsai':'Split', 'Foxtrot':'Breeze', 'Range': 'The Range'}

    awayScore = ''
    homeScore = ''

    try:

        async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/players/{playerID}', headers=headers, json={}) as r:
            data = await r.json(content_type='text/plain')
        matchID = data['MatchID']

        async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{matchID}', headers=headers, json={}) as r:
            data = await r.json(content_type='text/plain')

        try:
            if data['ProvisioningFlow'] == 'CustomGame':
                gameMode = 'Custom'
            else:
                gamefilesgameMode = data['MatchmakingData']['QueueID']
                gameMode = gamemodeTranslate[gamefilesgameMode]

            client = Client(region=region)
            client.activate()
            gameInfo = client.fetch_presence()
            homeScore, awayScore = gameInfo["partyOwnerMatchScoreAllyTeam"],gameInfo["partyOwnerMatchScoreEnemyTeam"]

        except:
            gameMode = ''

        gamefilesName = (data['MapID'].split('/'))[4]
        mapName = mapTranslations[gamefilesName]

    except:

        mapName = ''
        gameMode = ''

    if gamefilesState == 'Pregame':

        async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/pregame/v1/players/{playerID}', headers=headers, json={}) as r:
            data = await r.json(content_type='text/plain')
        pregameID = data['MatchID']

        async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/pregame/v1/matches/{pregameID}', headers=headers, json={}) as r:
            data = await r.json(content_type='text/plain')
        if data['ProvisioningFlowID'] == 'CustomGame':
            gameMode = 'Custom'
        else:
            gamefilesgameMode = data['QueueID']
            gameMode = gamemodeTranslate[gamefilesgameMode]
        gamefilesName = (data['MapID'].split('/'))[4]
        mapName = mapTranslations[gamefilesName]

    await session.close()

    return [state, mapName, gameMode, homeScore, awayScore]