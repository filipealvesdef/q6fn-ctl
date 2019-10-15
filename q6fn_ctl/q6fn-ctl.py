import asyncio
import websockets
import json
import ssl
import sys
import base64
import os
from wakeonlan import send_magic_packet

with open('config.json') as config:
    ip, mac, name = json.load(config).values()

port = '8002'
name = base64.b64encode(b'{name}').decode('utf-8')
token_path = 'token.txt'
token = None
url = f'wss://{ip}:{port}/api/v2/channels/samsung.remote.control?name={name}'
ssl_context = ssl.SSLContext()

if os.path.exists(token_path):
    with open(token_path) as f:
        token = f.read()

if token:
    url += f'&token={token}'

async def send_key(key, token):
    async with websockets.connect(url, ssl=ssl_context) as ws:
        r = await ws.recv()

        if not token:
            token = json.loads(r)['data']['token']
            with open('token.txt', 'w') as f:
                f.write(token)

        payload = json.dumps({
            "method": "ms.remote.control",
            "params": {
                "Cmd": "Click",
                "DataOfCmd": key,
                "Option": "false",
                "TypeOfRemote": "SendRemoteKey"
            }
        })
        await ws.send(payload)

key = sys.argv[1]
if key == 'POWERON':
    send_magic_packet(mac)
    key = 'KEY_POWER'

asyncio.get_event_loop().run_until_complete(send_key(key, token))
