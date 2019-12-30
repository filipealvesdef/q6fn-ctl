import asyncio
import websockets
import json
import ssl
import sys
import base64
import os
from wakeonlan import send_magic_packet

DIR_NAME = os.path.dirname(os.path.realpath(sys.argv[0]))
CONFIG_PATH = os.path.join(DIR_NAME, 'config.json')
TOKEN_PATH = os.path.join(DIR_NAME, 'token.txt')

with open(CONFIG_PATH) as config:
    ip, mac, name = json.load(config).values()

port = '8002'
name = base64.b64encode(bytes(name, encoding='ascii')).decode('utf-8')
token = None
url = f'wss://{ip}:{port}/api/v2/channels/samsung.remote.control?name={name}'
ssl_context = ssl.SSLContext()

if os.path.exists(TOKEN_PATH):
    with open(TOKEN_PATH) as f:
        token = f.read()

if token:
    url += f'&token={token}'

async def send_key(key, token):
    async with websockets.connect(url, ssl=ssl_context) as ws:
        r = await ws.recv()

        if not token:
            token = json.loads(r)['data']['token']
            with open(TOKEN_PATH, 'w') as f:
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
