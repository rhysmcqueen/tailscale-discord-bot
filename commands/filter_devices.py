def setup(bot, api_token, api_url):
    @bot.slash_command(name="filter_devices", description="Filter devices by a specific tag.")
    async def filter_devices(interaction, tag: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch data from Tailscale API.")
            return
        
        data = response.json()
        filtered_devices = [
            device for device in data.get("devices", []) if tag in device.get("tags", [])
        ]
        
        if not filtered_devices:
            await interaction.response.send_message(f"No devices found with tag '{tag}'.")
            return
        
        message = f"Devices with tag '{tag}':\n"
        for idx, device in enumerate(filtered_devices, start=1):
            message += (
                f"{idx}. Hostname: {device['hostname']}\n"
                f"   IP: {', '.join(device['addresses'])}\n"
                f"   OS: {device['os']}\n\n"
            )
        await interaction.response.send_message(message)
