def setup(bot, api_token, api_url):
    @bot.slash_command(name="suspend_user", description="Suspend a user from the Tailscale network.")
    async def suspend_user(interaction, user_email: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.post(f"{api_url}/users/{user_email}/suspend", headers=headers)
        
        if response.status_code == 200:
            await interaction.response.send_message(f"User {user_email} suspended successfully.")
        else:
            await interaction.response.send_message(f"Failed to suspend user. Error: {response.status_code}")
