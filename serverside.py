import asyncio
from websockets.asyncio.server import serve
import time
import random
import json

games = {}

async def create_game(wb):
    gid = random.randint(1000, 9999)
    while gid in games:
        gid = random.randint(1000, 9999)
    games[gid] = {'status': 'open', 'players': [wb]}
    await wb.send(json.dumps({'State': 'room_created', 'game_id': gid}))
    print(games)

async def manage_game(data, wb):
    pass

async def join_game(data, wb):
        gid = data['room_code']
        if gid in games and games[gid]['status'] == 'open':
            games[gid]['status'] = 'closed'
            games[gid]['players'].append(wb)
            await wb.send(json.dumps({'status': 202, 'message': 'joined sucessfully'}))
            await games[gid]['players'][0].send(json.dumps({'status': 202, 'message': 'game starting...'}))
            print(games)
        else:
            await wb.send(json.dumps({'status': 404, 'message': 'room not found or closed'}))


    

async def echoflow(websocket):
    async for message in websocket:
        data = json.loads(message)
        print('revived:', data, 'at', time.time())
        # Match the key case and only call the required coroutine
        state = data.get('State') or data.get('state')
        if state == 'create_room':
            await create_game(websocket)
        elif state == 'join_room':
            await join_game(data, websocket)
        elif state == 'in_game':
            await manage_game(data, websocket)

async def main():
    domain = 'localhost'
    port = 6666
    print(f'starting server... at {domain}:{port}')
    async with serve(echoflow, domain, port) as server:
        await server.serve_forever()   

if __name__ == "__main__":
    asyncio.run(main())