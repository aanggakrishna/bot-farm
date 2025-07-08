import os
import discord
import logging
from datetime import datetime
from discord.ext import commands
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

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    logging.info(f'Bot {bot.user} has connected to Discord!')

# Event: Message received
@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message is in the main channel
    if message.channel.id == int(os.getenv('CHANNEL_ID')):
        # Check if message is in the specified sub-channel
        if hasattr(message.channel, 'parent_id') and \
           message.channel.parent_id == int(os.getenv('SUB_CHANNEL_ID')):
            log_message = f'Message from {message.author} in sub-channel: {message.content}'
            print(log_message)
            logging.info(log_message)

    # Process commands if any
    await bot.process_commands(message)

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))