import nextcord
from nextcord.ext import commands, tasks
import requests
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
load_dotenv()

# Access the secrets
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TAILSCALE_API_TOKEN = os.getenv("TAILSCALE_API_TOKEN")
TAILSCALE_API_URL = os.getenv("TAILSCALE_API_URL")
GUILD_ID = int(os.getenv("GUILD_ID"))
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
# Bot setup
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_active_tailscale_clients():
    """
    Fetch active clients from the Tailscale API and log details for debugging.
    """
    headers = {"Authorization": f"Bearer {TAILSCALE_API_TOKEN}"}
    try:
        print("Fetching active clients from Tailscale API...")
        response = requests.get(TAILSCALE_API_URL, headers=headers)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # print("Response JSON:")
            # print(data)  # Logs the full API response for inspection Uncomment for troubleshooting

            # Define the time threshold for "active" devices (e.g., last seen within 5 minutes)
            active_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)

            # Filter for active clients based on `lastSeen`
            active_clients = [
                client for client in data.get("devices", [])
                if "lastSeen" in client and datetime.fromisoformat(client["lastSeen"].replace("Z", "+00:00")) > active_threshold
            ]

            print(f"Active Clients Count: {len(active_clients)}")
            return len(active_clients)
        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            return 0
    except requests.RequestException as e:
        print(f"Error while fetching data from Tailscale API: {e}")
        return 0
@tasks.loop(minutes=5)
async def update_bot_presence_and_channel():
    """
    Update the bot's presence and send a message to a channel with the active clients.
    """
    active_clients = get_active_tailscale_clients()
    activity = nextcord.Game(f"Active Tailscale clients: {active_clients}")
    await bot.change_presence(activity=activity)
    
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = guild.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"Currently, there are **{active_clients}** active Tailscale clients!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    update_bot_presence_and_channel.start()

# Run the bot
bot.run(BOT_TOKEN)
