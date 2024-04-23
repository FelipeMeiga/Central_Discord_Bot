from utils import *
from client import DiscordClient
import asyncio

#event_handle_example
async def handle_event(event_data) -> None:
    print(event_data)

if __name__ == "__main__":
    client = DiscordClient(TOKEN, "client_id_example", "guild_id_example")
    asyncio.run(client.connect(event_handle_function=handle_event))
