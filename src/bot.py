
import os
import json
import discord
from datetime import datetime

TOKEN = 'token'
# change the whitelisted server ids to all to log all servers, if not just add the server id
WHITELISTED_SERVER_IDS = 'all'

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'author': message.author.display_name,
        'content': message.content
    }
    
    if message.guild:
        if WHITELISTED_SERVER_IDS == 'all' or message.guild.id in WHITELISTED_SERVER_IDS:
            server_folder = f'/path/to/dir/{message.guild.name}({message.guild.id})'
            json_server_folder = f'/path/to/dir/{message.guild.name}({message.guild.id})'
            
            os.makedirs(server_folder, exist_ok=True)
            os.makedirs(json_server_folder, exist_ok=True)
            
            channel_file = f'{server_folder}/{message.channel.name}.txt'
            json_channel_file = f'{json_server_folder}/{message.channel.name}.json'
            
            with open(channel_file, 'a') as log_file:
                log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
                
            with open(json_channel_file, 'a') as json_log_file:
                json_log_file.write(json.dumps(log_entry) + '\n')
                
    elif message.guild is None and message.author != client.user:
        dm_folder = f'/path/to/dir/DM_{message.author.display_name}({message.author.display_name})'
        json_dm_folder = f'/path/to/dir/DM_{message.author.display_name}({message.author.display_name})'
        
        os.makedirs(dm_folder, exist_ok=True)
        os.makedirs(json_dm_folder, exist_ok=True)
        
        dm_file = f'{dm_folder}/DM.txt'
        json_dm_file = f'{json_dm_folder}/DM.json'
        
        with open(dm_file, 'a') as log_file:
            log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
            
        with open(json_dm_file, 'a') as json_log_file:
            json_log_file.write(json.dumps(log_entry) + '\n')

client.run(TOKEN)

