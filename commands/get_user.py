def setup(bot, api_token, api_url):
    @bot.slash_command(name="get_user", description="Fetch details of a specific user.")
    async def get_user(interaction, user_email: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(f"{api_url}/users/{user_email}", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            message = f"User Details:\nEmail: {user_email}\nRole: {user_data['role']}\n"
            await interaction.response.send_message(message)
        else:
            await interaction.response.send_message(f"Failed to fetch user details. Error: {response.status_code}")
