import asyncio
from websockets.asyncio.server import serve
import datetime
import random
import json

games = {}

async def create_game(wb):
    gid = str(random.randint(1000, 9999))
    while gid in games:
        gid = str(random.randint(1000, 9999))
    games[gid] = {'Condition': 'open', 'players': [wb]}
    await wb.send(json.dumps({'State': 'room_created', 'game_id': gid}))
    print(games)

async def manage_game(data, wb):
    game_id  = data['room_code']
    change = data['change']
    for player in games[game_id]['players']:
        if player != wb:
            await player.send(json.dumps({'change': change}))



async def join_game(data, wb):
        gid = data['room_code']
        if (gid in games) and (games[gid]['Condition'] == 'open'):
            games[gid]['Condition'] = 'closed'
            games[gid]['players'].append(wb)
            await wb.send(json.dumps({'State': 'room_ready'}))
            await games[gid]['players'][0].send(json.dumps({'State': 'room_ready'}))
            print(games)
        else:
            await wb.send(json.dumps({'State': 'room_not_found / room_closed'}))


    

async def echoflow(websocket):
    async for message in websocket:
        data = json.loads(message)
        print('revived:', data, 'at', datetime.datetime.now())
        try:
            state = data.get('State')
        except:
            ...
        if state == 'create_room':
            await create_game(websocket)
        elif state == 'join_room':
            await join_game(data, websocket)
        elif state == 'game_send':
            await manage_game(data, websocket)
        else:
            ...

async def main():
    domain = 'localhost'
    port = 6666
    print(f'starting server... at {domain}:{port}')
    async with serve(echoflow, domain, port) as server:
        await server.serve_forever()   

if __name__ == "__main__":
    asyncio.run(main())