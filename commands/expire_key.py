def setup(bot, api_token, api_url):
    @bot.slash_command(name="expire_key", description="Expire a device's key.")
    async def expire_key(interaction, device_id: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.post(f"{api_url}/{device_id}/expire-key", headers=headers)
        
        if response.status_code == 200:
            await interaction.response.send_message(f"Key for device {device_id} expired successfully.")
        else:
            await interaction.response.send_message(f"Failed to expire key. Error: {response.status_code}")
