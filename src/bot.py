import os
import json
import discord
from datetime import datetime

TOKEN = 'your_bot_token'
WHITELISTED_SERVER_IDS = 'all'

# Define constants for log directory paths
LOG_DIR = '/path/to/dir/'
SERVER_LOG_DIR = os.path.join(LOG_DIR, 'server_logs')
JSON_SERVER_LOG_DIR = os.path.join(LOG_DIR, 'json_server_logs')
DM_LOG_DIR = os.path.join(LOG_DIR, 'dm_logs')
JSON_DM_LOG_DIR = os.path.join(LOG_DIR, 'json_dm_logs')

client = discord.Client()

@client.event
async def on_ready():
    # Print a message when the bot is ready and logged in
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
            # Create folders for server logs
            server_folder = os.path.join(SERVER_LOG_DIR, f'{message.guild.name}({message.guild.id})')
            json_server_folder = os.path.join(JSON_SERVER_LOG_DIR, f'{message.guild.name}({message.guild.id})')
            
            try:
                os.makedirs(server_folder, exist_ok=True)
                os.makedirs(json_server_folder, exist_ok=True)
                
                channel_file = os.path.join(server_folder, f'{message.channel.name}.txt')
                json_channel_file = os.path.join(json_server_folder, f'{message.channel.name}.json')
                
                with open(channel_file, 'a') as log_file:
                    log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
                    
                with open(json_channel_file, 'a') as json_log_file:
                    json_log_file.write(json.dumps(log_entry) + '\n')
            except Exception as e:
                # Handle errors related to file operations
                print(f'Error writing to {channel_file}: {e}')
                
    elif message.guild is None and message.author != client.user:
        # Create folders for direct message logs
        dm_folder = os.path.join(DM_LOG_DIR, f'DM_{message.author.display_name}({message.author.id})')
        json_dm_folder = os.path.join(JSON_DM_LOG_DIR, f'DM_{message.author.display_name}({message.author.id})')
        
        try:
            os.makedirs(dm_folder, exist_ok=True)
            os.makedirs(json_dm_folder, exist_ok=True)
            
            dm_file = os.path.join(dm_folder, 'DM.txt')
            json_dm_file = os.path.join(json_dm_folder, 'DM.json')
            
            with open(dm_file, 'a') as log_file:
                log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
                
            with open(json_dm_file, 'a') as json_log_file:
                json_log_file.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            # Handle errors related to file operations
            print(f'Error writing to {dm_file}: {e}')

client.run(TOKEN)