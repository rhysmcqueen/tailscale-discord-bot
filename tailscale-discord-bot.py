import os
import requests
from datetime import datetime, timedelta, timezone
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Bot and Tailscale settings
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TAILSCALE_API_TOKEN = os.getenv("TAILSCALE_API_TOKEN")
TAILSCALE_API_URL = os.getenv("TAILSCALE_API_URL")

# Bot setup
intents = nextcord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def fetch_tailscale_data():
    headers = {"Authorization": f"Bearer {TAILSCALE_API_TOKEN}"}
    try:
        response = requests.get(TAILSCALE_API_URL, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching Tailscale data: {e}")
        return None

@bot.slash_command(name="active_devices", description="List all currently active devices on Tailscale.")
async def active_devices(interaction: Interaction):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    active_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)
    active_clients = [
        client for client in data.get("devices", [])
        if "lastSeen" in client and datetime.fromisoformat(client["lastSeen"].replace("Z", "+00:00")) > active_threshold
    ]

    if not active_clients:
        await interaction.response.send_message("No active devices found.")
        return

    message = "Active Devices:\n"
    for idx, client in enumerate(active_clients, start=1):
        message += f"{idx}. Hostname: {client['hostname']}\n   IP: {', '.join(client['addresses'])}\n   OS: {client['os']}\n   Last Seen: {client['lastSeen']}\n\n"

    await interaction.response.send_message(message)

@bot.slash_command(name="device_details", description="Get details of a specific device.")
async def device_details(
    interaction: Interaction,
    device: str = SlashOption(
        description="Choose a device",
        autocomplete=True
    )
):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    selected_device = next((client for client in data.get("devices", []) if client["hostname"] == device), None)
    if not selected_device:
        await interaction.response.send_message(f"Device '{device}' not found.")
        return

    message = (
        f"Device Details:\n"
        f"Hostname: {selected_device['hostname']}\n"
        f"IP: {', '.join(selected_device['addresses'])}\n"
        f"OS: {selected_device['os']}\n"
        f"Client Version: {selected_device['clientVersion']}\n"
        f"Last Seen: {selected_device['lastSeen']}\n"
        f"Tags: {', '.join(selected_device.get('tags', []))}\n"
    )

    await interaction.response.send_message(message)

@device_details.on_autocomplete("device")
async def autocomplete_device(interaction: Interaction, value: str):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    suggestions = [
        client["hostname"]
        for client in data.get("devices", [])
        if value.lower() in client["hostname"].lower()
    ][:25]

    await interaction.response.send_autocomplete(suggestions)

@bot.slash_command(name="list_tags", description="List all available tags in the Tailscale network.")
async def list_tags(interaction: Interaction):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    tags = set(tag for client in data.get("devices", []) for tag in client.get("tags", []))

    if not tags:
        await interaction.response.send_message("No tags found in the network.")
        return

    message = "Available Tags:\n" + "\n".join(f"- {tag}" for tag in tags)
    await interaction.response.send_message(message)

@bot.slash_command(name="filter_devices", description="Filter devices by a tag.")
async def filter_devices(
    interaction: Interaction,
    tag: str = SlashOption(description="Enter a tag to filter devices")
):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    filtered_devices = [
        client for client in data.get("devices", []) if tag in client.get("tags", [])
    ]

    if not filtered_devices:
        await interaction.response.send_message(f"No devices found with tag '{tag}'.")
        return

    message = f"Devices with tag '{tag}':\n"
    for idx, client in enumerate(filtered_devices, start=1):
        message += f"{idx}. Hostname: {client['hostname']}\n   IP: {', '.join(client['addresses'])}\n   OS: {client['os']}\n\n"

    await interaction.response.send_message(message)

@bot.slash_command(name="list_users", description="List all users in the Tailscale network.")
async def list_users(interaction: Interaction):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    users = set(client["user"] for client in data.get("devices", []))

    if not users:
        await interaction.response.send_message("No users found in the network.")
        return

    message = "Users:\n" + "\n".join(f"- {user}" for user in users)
    await interaction.response.send_message(message)

@bot.slash_command(name="network_status", description="Get a summary of the network status.")
async def network_status(interaction: Interaction):
    data = fetch_tailscale_data()
    if not data:
        await interaction.response.send_message("Failed to fetch data from Tailscale API.")
        return

    total_devices = len(data.get("devices", []))
    active_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)
    active_devices = [
        client for client in data.get("devices", [])
        if "lastSeen" in client and datetime.fromisoformat(client["lastSeen"].replace("Z", "+00:00")) > active_threshold
    ]

    message = (
        f"Network Status:\n"
        f"Total Devices: {total_devices}\n"
        f"Active Devices: {len(active_devices)}\n"
    )

    await interaction.response.send_message(message)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

    try:
        # Sync slash commands
        synced = await bot.sync_application_commands()
        if synced is not None:
            print(f"Slash commands synced: {len(synced)} commands")
        else:
            print("No new commands to sync.")
    except Exception as e:
        print(f"Error syncing slash commands: {e}")

bot.run(BOT_TOKEN)
