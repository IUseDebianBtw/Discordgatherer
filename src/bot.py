import os
import discord.pyself
from datetime import datetime

TOKEN = 'your_bot_token_here'

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.guild and message.guild in client.guilds:
        
        server_folder = f'server_{message.guild.id}'
        os.makedirs(server_folder, exist_ok=True)

        channel_file = f'{server_folder}/{message.channel.name}.txt'

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Create a timestamp

        with open(channel_file, 'a') as log_file:
            log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')

    elif message.guild is None and message.author != client.user:
        dm_folder = f'DM_{message.author.id}'
        os.makedirs(dm_folder, exist_ok=True)
        dm_file = f'{dm_folder}/DM.txt'
        
        with open(dm_file, 'a') as log_file:
            log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')

client.run(TOKEN)

