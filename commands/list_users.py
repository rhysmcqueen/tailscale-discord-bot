def setup(bot, api_token, api_url):
    @bot.slash_command(name="list_users", description="List all users in the Tailscale network.")
    async def list_users(interaction):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            await interaction.response.send_message("Failed to fetch data from Tailscale API.")
            return
        
        data = response.json()
        users = {device["user"] for device in data.get("devices", [])}
        
        if not users:
            await interaction.response.send_message("No users found in the network.")
            return
        
        message = "Users:\n" + "\n".join(f"- {user}" for user in users)
        await interaction.response.send_message(message)
