def setup(bot, api_token, api_url):
    @bot.slash_command(name="set_device_routes", description="Enable or disable a route for a specific device.")
    async def set_device_routes(interaction, device_id: str, route: str, enable: bool):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        data = {"route": route, "enabled": enable}
        response = requests.post(f"{api_url}/{device_id}/routes", json=data, headers=headers)
        
        if response.status_code == 200:
            action = "enabled" if enable else "disabled"
            await interaction.response.send_message(f"Route {route} {action} successfully.")
        else:
            await interaction.response.send_message(f"Failed to set route. Error: {response.status_code}")
