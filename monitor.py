import os
import discord
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a new log file for each session with timestamp
session_start = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_directory, f'discord_monitor_{session_start}.log')

# Configure logging with more detailed format
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - User: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configure console handler for real-time display
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S')
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)

# Client configuration
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Enable member tracking
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    startup_message = f'Monitoring started as {client.user}'
    print('=' * 50)
    print(startup_message)
    print(f'Log file: {log_file}')
    print('=' * 50)
    logging.info(startup_message)

@client.event
async def on_message(message):
    # Check if message is in the target thread/channel
    if message.channel.id == int(os.getenv('SUB_CHANNEL_ID')):
        # Get user details
        user_name = message.author.name
        user_id = message.author.id
        
        # Log the message with user details
        log_message = f'{user_name}({user_id}): {message.content}'
        logging.info(log_message)
        
        # Log attachments if any
        if message.attachments:
            for attachment in message.attachments:
                attachment_log = f'{user_name} shared: {attachment.url}'
                logging.info(attachment_log)

@client.event
async def on_message_edit(before, after):
    # Check if edited message is in the target thread/channel
    if after.channel.id == int(os.getenv('SUB_CHANNEL_ID')):
        edit_log = f'{after.author.name} edited message: "{before.content}" -> "{after.content}"'
        logging.info(edit_log)

@client.event
async def on_message_delete(message):
    # Check if deleted message was in the target thread/channel
    if message.channel.id == int(os.getenv('SUB_CHANNEL_ID')):
        delete_log = f'{message.author.name} deleted message: "{message.content}"'
        logging.info(delete_log)

@client.event
async def on_member_join(member):
    join_log = f'User {member.name}({member.id}) joined the server'
    logging.info(join_log)

@client.event
async def on_member_remove(member):
    remove_log = f'User {member.name}({member.id}) left the server'
    logging.info(remove_log)

# Run the client
try:
    client.run(os.getenv('DISCORD_USER_TOKEN'))
except Exception as e:
    logging.error(f'Failed to start monitor: {str(e)}')
    print(f'Error: {str(e)}')