import os
import discord
from datetime import datetime

TOKEN = 'your_bot_token'
# change the whitelisted server ids to all to log all servers, if not just add the server id
WHITELISTED_SERVER_IDS = [12345679, 123465976]

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if message.guild:
        if WHITELISTED_SERVER_IDS == 'all' or message.guild.id in WHITELISTED_SERVER_IDS:
            server_folder = f'/path/to/dir/{message.guild.id}'
            os.makedirs(server_folder, exist_ok=True)
            channel_file = f'{server_folder}/{message.channel.name}.md'
            
            with open(channel_file, 'a') as log_file:
                log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
                
    elif message.guild is None and message.author != client.user:
        dm_folder = f'/path/to/dir/DM_{message.author.id}'
        os.makedirs(dm_folder, exist_ok=True)
        dm_file = f'{dm_folder}/DM.md'
        
        with open(dm_file, 'a') as log_file:
            log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')

client.run(TOKEN)
