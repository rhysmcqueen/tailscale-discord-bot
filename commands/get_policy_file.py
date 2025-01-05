def setup(bot, api_token, api_url):
    @bot.slash_command(name="get_policy_file", description="Retrieve the network's ACL policy file.")
    async def get_policy_file(interaction):
        import requests
        headers = {"Authorization": f"Bearer {api_token}"}
        response = requests.get(f"{api_url}/acl", headers=headers)
        
        if response.status_code == 200:
            policy_file = response.json()
            await interaction.response.send_message(f"Policy File:\n{policy_file}")
        else:
            await interaction.response.send_message(f"Failed to retrieve policy file. Error: {response.status_code}")
