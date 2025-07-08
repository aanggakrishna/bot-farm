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

log_file = os.path.join(log_directory, f'discord_thread_messages_{datetime.now().strftime("%Y%m%d")}.log')
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

async def fetch_thread_messages():
    # Get the channel
    channel = client.get_channel(int(os.getenv('CHANNEL_ID')))
    if not channel:
        print(f'Channel not found')
        return

    # Get the thread
    thread = None
    for thread_channel in channel.threads:
        if thread_channel.id == int(os.getenv('SUB_CHANNEL_ID')):
            thread = thread_channel
            break

    if not thread:
        print(f'Thread not found')
        return

    print(f'Fetching messages from thread: {thread.name}')
    logging.info(f'Fetching messages from thread: {thread.name}')

    # Fetch message history
    async for message in thread.history(limit=None):
        log_message = f'Message from {message.author} at {message.created_at}: {message.content}'
        print(log_message)
        logging.info(log_message)

        # Log attachments if any
        if message.attachments:
            for attachment in message.attachments:
                attachment_log = f'Attachment from {message.author}: {attachment.url}'
                print(attachment_log)
                logging.info(attachment_log)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    logging.info(f'Logged in as {client.user}')
    
    # Fetch thread messages when client is ready
    await fetch_thread_messages()
    
    # Optional: Keep monitoring for new messages
    print('Now monitoring for new messages...')

@client.event
async def on_message(message):
    # Check if message is in the target thread
    if message.channel.id == int(os.getenv('SUB_CHANNEL_ID')):
        log_message = f'New message from {message.author}: {message.content}'
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