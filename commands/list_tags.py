def setup(bot, api_token, api_url):
    @bot.slash_command(name="list_tags", description="List all available tags in the Tailscale network.")
    async def list_tags(interaction):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch data from Tailscale API.")
            return
        
        data = response.json()
        tags = {tag for device in data.get("devices", []) for tag in device.get("tags", [])}
        
        if not tags:
            await interaction.response.send_message("No tags found in the network.")
            return
        
        message = "Available Tags:\n" + "\n".join(f"- {tag}" for tag in tags)
        await interaction.response.send_message(message)
