def setup(bot, api_token, api_url):
    @bot.slash_command(name="device_details", description="Get details of a specific device.")
    async def device_details(interaction, device: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch data from Tailscale API.")
            return

        data = response.json()
        selected_device = next((d for d in data.get("devices", []) if d["hostname"] == device), None)

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
