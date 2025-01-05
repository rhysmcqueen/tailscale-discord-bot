def setup(bot, api_token, api_url):
    @bot.slash_command(name="network_status", description="Get a summary of the network's status.")
    async def network_status(interaction):
        import requests
        from datetime import datetime, timedelta, timezone
        
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch data from Tailscale API.")
            return
        
        data = response.json()
        total_devices = len(data.get("devices", []))
        active_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)
        active_devices = [
            device for device in data.get("devices", [])
            if "lastSeen" in device and datetime.fromisoformat(device["lastSeen"].replace("Z", "+00:00")) > active_threshold
        ]
        
        message = (
            f"Network Status:\n"
            f"Total Devices: {total_devices}\n"
            f"Active Devices: {len(active_devices)}\n"
        )
        await interaction.response.send_message(message)
