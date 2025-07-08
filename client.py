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

log_file = os.path.join(log_directory, f'discord_messages_{datetime.now().strftime("%Y%m%d")}.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Client configuration
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    logging.info(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    # Check if message is in the main channel
    if message.channel.id == int(os.getenv('CHANNEL_ID')):
        # Check if message is in the specified sub-channel
        if hasattr(message.channel, 'parent_id') and \
           message.channel.parent_id == int(os.getenv('SUB_CHANNEL_ID')):
            log_message = f'Message from {message.author} in sub-channel: {message.content}'
            print(log_message)
            logging.info(log_message)
            
            # Log attachments if any
            if message.attachments:
                for attachment in message.attachments:
                    attachment_log = f'Attachment from {message.author}: {attachment.url}'
                    print(attachment_log)
                    logging.info(attachment_log)

# Run the client
client.run(os.getenv('DISCORD_USER_TOKEN'))