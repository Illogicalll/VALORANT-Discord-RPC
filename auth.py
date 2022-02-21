import aiohttp
import re

async def userAuth(username, password):
    session = aiohttp.ClientSession()

    data = {'client_id': 'play-valorant-web-prod',
            'nonce': '1',
            'redirect_uri': 'https://playvalorant.com/opt_in',
            'response_type': 'token id_token'}
    
    headers = {"Accept": "*/*",
               "User-Agent": username}

    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)

    data = {'type': 'auth',
            'username': username,
            'password': password}
    
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers) as r:
        data = await r.json()
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    accessToken = data[0]

    headers = {'Authorization': f'Bearer {accessToken}',
               "User-Agent": username}

    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlementsToken = data['entitlements_token']

    headers = {'Authorization': f'Bearer {accessToken}'}

    async with session.get('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    puuid = data['sub']
    
    await session.close()
    
    return [accessToken, entitlementsToken, puuid]