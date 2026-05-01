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
    wb.send({'status':201 , 'message':'game created sucessfully', 'game_id':gid})

async def manage_games(msg, wb):
    if msg['game_id']:
        gid = msg['game_id']
        if msg['JoinReq'] and games[gid]['status'] == 'closed':
            wb.send({'status':204  , 'message':'game is full!'})
        if msg['JoinReq'] and games[gid]['status'] == 'open':
            games[gid]['status'] = 'closed'
            games[gid]['players'].append(wb)
            wb.send({'status':202 , 'message':'joined sucessfully'})
            games[gid]['players'][0].send({'status':202 , 'message':'game starting...'})
        else:
            ...

    else:
        create_game(wb)

    

async def echoflow(websocket):
    async for message in websocket:
        message = json.loads(message)
        print('revived:', message, 'at', time.time())
        await manage_games(message, websocket)

async def main():
    domain = 'localhost'
    port = 6666
    print(f'starting server... at {domain}:{port}')
    async with serve(echoflow, domain, port) as server:
        await server.serve_forever()   

if __name__ == "__main__":
    asyncio.run(main())