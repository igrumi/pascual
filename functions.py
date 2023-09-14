import random

async def handle_custom_response(message, response):
    print(f"\nMessage content: {message.content}")
    print(f"Server: {message.guild.name}")
    print(f"Author ID: {message.author.id}")

    # Get the guild where the command was invoked
    guild = message.guild

    # Check if the user with user_id is a member of the guild
    user = guild.get_member(response['user_id'])

    if user:
        response_type = response.get('type', 'text')
        if response.get('random', False):
            responses = response.get('responses', [])
            if responses:
                random_response = random.choice(responses)
                await message.channel.send(f"<@{response['user_id']}> {random_response}")
            else:
                await message.channel.send(f"<@{response['user_id']}> No responses defined.")

        elif response_type == 'ping':
            await message.channel.send(f"<@{response['user_id']}>")

        elif response_type == 'text':
            await message.channel.send(f"<@{response['user_id']}> {response['content']}")

        elif response_type == 'emoji':
            await message.channel.send(f"<@{response['user_id']}> {response['emoji']}")

        elif response_type == 'emoji3':
            await message.channel.send(f"<@{response['user_id']}> {response['emoji']} {response['emoji']} {response['emoji']}")

        elif response_type == 'gif':
            await message.channel.send(f"<@{response['user_id']}>")
            await message.channel.send(response['gif_url'])

        elif response_type == 'textmoji3':
            await message.channel.send(f"<@{response['user_id']}> {response['content']} {response['emoji']} {response['emoji']} {response['emoji']}")

        elif response_type == 'textmoji':
            await message.channel.send(f"<@{response['user_id']}> {response['content']} {response['emoji']}")

    else:
        await message.channel.send(f"User to ping not found in the server")

async def process_message(message, keyword_responses, bot):
    # Check if the message content contains any of the specified keywords
    if message.content.startswith(bot.command_prefix):
        # Handle bot commands here
        await bot.process_commands(message)
        return
    content_lower = message.content.lower()

    for keyword, response in keyword_responses.items():
        if keyword in content_lower:
            await handle_custom_response(message, response)