from datetime import datetime, timedelta, timezone
import requests
from nextcord import Interaction  # Import Interaction

def setup(bot, api_token, api_url):
    @bot.slash_command(name="active_devices", description="List all currently active devices on Tailscale.")
    async def active_devices(interaction: Interaction):  # Use Interaction here
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch data from Tailscale API.")
            return

        data = response.json()
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
            message += (
                f"{idx}. Hostname: {client['hostname']}\n"
                f"   IP: {', '.join(client['addresses'])}\n"
                f"   OS: {client['os']}\n"
                f"   Last Seen: {client['lastSeen']}\n\n"
            )

        await interaction.response.send_message(message)
