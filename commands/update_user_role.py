def setup(bot, api_token, api_url):
    @bot.slash_command(name="update_user_role", description="Update the role of a specific user.")
    async def update_user_role(interaction, user_email: str, new_role: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        data = {"role": new_role}
        response = requests.patch(f"{api_url}/users/{user_email}", json=data, headers=headers)
        
        if response.status_code == 200:
            await interaction.response.send_message(f"User role updated successfully to {new_role}.")
        else:
            await interaction.response.send_message(f"Failed to update user role. Error: {response.status_code}")
