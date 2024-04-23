import asyncio
import websockets #type:ignore
import json
from utils import *

class DiscordClient:
    def __init__(self, token, client_id, guild_id) -> None:
        self.token = token
        self.uri = URI
        self.base_url = BASE_URL
        self.client_id = client_id
        self.guild_id = guild_id
        self.headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
        self.intents = (
            (1 << 0) |  # GUILDS
            (1 << 1) |  # GUILD_MEMBERS (Privilegiado)
            (1 << 2) |  # GUILD_BANS
            (1 << 3) |  # GUILD_EMOJIS_AND_STICKERS
            (1 << 4) |  # GUILD_INTEGRATIONS
            (1 << 5) |  # GUILD_WEBHOOKS
            (1 << 6) |  # GUILD_INVITES
            (1 << 7) |  # GUILD_VOICE_STATES
            (1 << 8) |  # GUILD_PRESENCES (Privilegiado)
            (1 << 9) |  # GUILD_MESSAGES
            (1 << 10) | # GUILD_MESSAGE_REACTIONS
            (1 << 11) | # GUILD_MESSAGE_TYPING
            (1 << 12) | # DIRECT_MESSAGES
            (1 << 13) | # DIRECT_MESSAGE_REACTIONS
            (1 << 14) | # DIRECT_MESSAGE_TYPING
            (1 << 15)   # MESSAGE_CONTENT
        )

    async def connect(self, event_handle_function) -> None:
        async with websockets.connect(self.uri) as websocket:
            self.websocket = websocket
            greeting = await websocket.recv()
            await self.on_hello(json.loads(greeting))
            asyncio.create_task(self.send_heartbeat())
            await self.process_events(event_handle_function)


    async def on_hello(self, greeting_data) -> None:
        self.heartbeat_interval = greeting_data["d"]["heartbeat_interval"] / 1000
        print("[+] Received Hello:", greeting_data)
        await self.identify()

    async def send_heartbeat(self) -> None:
        heartbeat_json = json.dumps({
            "op": 1,
            "d": None
        })
        while True:
            #print("Sending heartbeat")
            await self.websocket.send(heartbeat_json)
            await asyncio.sleep(self.heartbeat_interval)

    async def identify(self) -> None:
        identify_json = json.dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "my_custom_bot",
                    "$device": "my_custom_bot"
                }
            }
        })
        print("[+] Sending identify payload")
        await self.websocket.send(identify_json)

    async def process_events(self, handle_event) -> None:
        async for message in self.websocket:
            data = json.loads(message)
            await handle_event(data)
    