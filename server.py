import asyncio
from websockets.asyncio.server import serve, ServerConnection
from websockets.exceptions import ConnectionClosedOK

sockets = {}
async def handler(websocket: ServerConnection):
    client_host, client_port, *_ = websocket.remote_address
    sockets[f'{client_host}:{client_port}'] = websocket
    print(f'{client_host}:{client_port}')

    try:
        print(sockets)
        async for message in websocket:
            for socket in sockets.values():
                await socket.send(message)
    
    except ConnectionClosedOK:
        print('connection closed')
        sockets.clear()
    
    finally:
        del sockets[f'{client_host}:{client_port}']


async def main():
    async with serve(handler, 'localhost', 8999):
        await asyncio.get_running_loop().create_future()


asyncio.run(main())
