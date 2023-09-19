import os
import discord
from datetime import datetime

TOKEN = 'your_bot_token'
WHITELISTED_SERVER_IDS = [12345679, 123465976]

# Define constants for log directory paths
LOG_DIR = '/path/to/dir/'
SERVER_LOG_DIR = os.path.join(LOG_DIR, 'server_logs')
DM_LOG_DIR = os.path.join(LOG_DIR, 'dm_logs')

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if message.guild:
        if WHITELISTED_SERVER_IDS == 'all' or message.guild.id in WHITELISTED_SERVER_IDS:
            server_folder = os.path.join(SERVER_LOG_DIR, str(message.guild.id))
            try:
                os.makedirs(server_folder, exist_ok=True)
                channel_file = os.path.join(server_folder, f'{message.channel.name}.md')
                
                with open(channel_file, 'a') as log_file:
                    log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
            except Exception as e:
                print(f'Error writing to {channel_file}: {e}')
                
    elif message.guild is None and message.author != client.user:
        dm_folder = os.path.join(DM_LOG_DIR, f'DM_{message.author.id}')
        try:
            os.makedirs(dm_folder, exist_ok=True)
            dm_file = os.path.join(dm_folder, 'DM.md')
            
            with open(dm_file, 'a') as log_file:
                log_file.write(f'{timestamp} | {message.author.display_name}: {message.content}\n')
        except Exception as e:
            print(f'Error writing to {dm_file}: {e}')

client.run(TOKEN)
