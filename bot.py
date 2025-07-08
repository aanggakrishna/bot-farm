import os
import discord
import logging
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Logging Configuration ---
log_directory = 'logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Create a new log file for each session with timestamp
session_start = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_directory, f'discord_bot_{session_start}.log')

# Configure file handler
file_handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s: %(message)s'))

# Configure console handler for real-time display
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s', datefmt='%H:%M:%S'))

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

# --- Bot Configuration ---
# Privileged intents (members, message_content) must be enabled in the Discord Developer Portal
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Environment variable check
TOKEN = os.getenv('DISCORD_TOKEN')
MONITORED_THREAD_ID_STR = os.getenv('SUB_CHANNEL_ID')

if not TOKEN:
    logging.critical("DISCORD_TOKEN environment variable not set. Bot cannot start.")
    exit()
if not MONITORED_THREAD_ID_STR:
    logging.critical("SUB_CHANNEL_ID environment variable not set. Bot cannot start.")
    exit()

try:
    MONITORED_THREAD_ID = int(MONITORED_THREAD_ID_STR)
except ValueError:
    logging.critical("SUB_CHANNEL_ID must be a valid integer ID.")
    exit()

# --- Events ---
@bot.event
async def on_ready():
    startup_message = f'{bot.user} has connected to Discord and is ready to monitor!'
    print('=' * 60)
    print(startup_message)
    print(f'Monitoring Thread ID: {MONITORED_THREAD_ID}')
    print(f'Log file: {log_file}')
    print('=' * 60)
    logging.info(startup_message)

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    # Check if message is in the target thread
    if message.channel.id == MONITORED_THREAD_ID:
        user_name = f'{message.author.name}#{message.author.discriminator}'
        log_message = f'New Message - {user_name} ({message.author.id}): {message.content}'
        logging.info(log_message)
        
        # Log attachments if any
        if message.attachments:
            for attachment in message.attachments:
                attachment_log = f'Attachment from {user_name}: {attachment.url}'
                logging.info(attachment_log)

    # Process commands
    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return
    if after.channel.id == MONITORED_THREAD_ID:
        user_name = f'{after.author.name}#{after.author.discriminator}'
        edit_log = f'Message Edit - {user_name} edited: "{before.content}" -> "{after.content}"'
        logging.info(edit_log)

@bot.event
async def on_message_delete(message):
    if message.channel.id == MONITORED_THREAD_ID:
        user_name = f'{message.author.name}#{message.author.discriminator}'
        delete_log = f'Message Delete - {user_name} deleted: "{message.content}"'
        logging.info(delete_log)

@bot.event
async def on_member_join(member):
    join_log = f'Member Join - {member.name}#{member.discriminator} ({member.id}) joined the server.'
    logging.info(join_log)

@bot.event
async def on_member_remove(member):
    remove_log = f'Member Leave - {member.name}#{member.discriminator} ({member.id}) left the server.'
    logging.info(remove_log)

# --- Commands ---
@bot.command(name='fetch_history')
@commands.has_permissions(manage_messages=True) # Only allow users who can manage messages to run this
async def fetch_history(ctx, limit: int = 100):
    """Fetches the last 'limit' messages from the monitored thread."""
    if ctx.channel.id != MONITORED_THREAD_ID:
        await ctx.send("This command can only be used in the monitored thread.", delete_after=10)
        return

    await ctx.send(f"Fetching last {limit} messages... This may take a moment.", delete_after=5)
    
    history_log_file = os.path.join(log_directory, f'history_fetch_{session_start}.log')
    
    try:
        with open(history_log_file, 'w', encoding='utf-8') as f:
            f.write(f"Message history for thread '{ctx.channel.name}' ({ctx.channel.id}) fetched at {datetime.now()}\n")
            f.write("="*50 + "\n")
            
            count = 0
            async for message in ctx.channel.history(limit=limit):
                user_name = f'{message.author.name}#{message.author.discriminator}'
                log_line = f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {user_name}: {message.content}\n"
                f.write(log_line)
                if message.attachments:
                    for att in message.attachments:
                        f.write(f"  [Attachment] {att.url}\n")
                count += 1
        
        logging.info(f"Successfully fetched and saved {count} messages to {history_log_file}")
        await ctx.send(f"Successfully saved {count} messages to `{history_log_file}`.", delete_after=20)

    except Exception as e:
        logging.error(f"Failed to fetch message history: {e}")
        await ctx.send(f"An error occurred while fetching history. Check logs.", delete_after=10)

# --- Main Execution ---
if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except discord.errors.LoginFailure:
        logging.critical("Login failed: Improper token. Please ensure your DISCORD_TOKEN in the .env file is a valid BOT token from the Discord Developer Portal.")
    except discord.errors.PrivilegedIntentsRequired:
        logging.critical("Privileged Intents Required: Please enable 'Server Members Intent' and 'Message Content Intent' for your bot in the Discord Developer Portal.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}")