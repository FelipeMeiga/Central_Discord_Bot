from utils import *
from client import DiscordClient
import asyncio

client = DiscordClient(TOKEN, "client_id_example", "guild_id_example")

#event_handle_example
async def handle_event(event_data) -> None:
    print(event_data)
    
    if event_data['t'] == 'INTERACTION_CREATE':
        await handle_interaction(event_data['d'])

async def handle_interaction(interaction):
    interaction_id = interaction['id']
    interaction_token = interaction['token']
    command_name = interaction['data']['name']

    if command_name == "hello":
        await client.send_interaction_response(interaction_id, interaction_token, "Hello Central!")

async def main():
    #await client.register_slash_command("", "")
    await client.connect(event_handle_function=handle_event)

if __name__ == "__main__":
    asyncio.run(main())
