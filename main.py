import os
import importlib
from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
from nextcord import Interaction

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TAILSCALE_API_TOKEN = os.getenv("TAILSCALE_API_TOKEN")
TAILSCALE_API_URL = os.getenv("TAILSCALE_API_URL")

# Initialize the bot
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Dynamically load commands from the commands folder
commands_folder = "commands"

for filename in os.listdir(commands_folder):
    if filename.endswith(".py"):
        command_name = filename[:-3]  # Remove the .py extension
        module = importlib.import_module(f"{commands_folder}.{command_name}")
        module.setup(bot, TAILSCALE_API_TOKEN, TAILSCALE_API_URL)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# Run the bot
bot.run(BOT_TOKEN)
