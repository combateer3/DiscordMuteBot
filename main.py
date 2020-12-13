import json
import discord

with open('secrets.json') as file:
    data = json.load(file)

TOKEN = data['bot_token']

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


client.run(TOKEN)
