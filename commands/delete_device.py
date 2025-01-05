def setup(bot, api_token, api_url):
    @bot.slash_command(name="remove_device", description="Delete a device from the Tailscale network.")
    async def remove_device(interaction, device_id: str):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.delete(f"{api_url}/{device_id}", headers=headers)
        
        if response.status_code == 200:
            await interaction.response.send_message(f"Device with ID {device_id} deleted successfully.")
        else:
            await interaction.response.send_message(f"Failed to delete device. Error: {response.status_code}")
