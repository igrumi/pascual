import discord
import os
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Enable guild (server) join and leave events
intents.members = True  # Enable member-related events
intents.dm_messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

close = [710679721859612682]

# Fetch a random image from Unsplash using the given keyword
def get_unsplash_image(keyword):
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    url = f"https://api.unsplash.com/photos/random?query={keyword}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data["urls"]["regular"]
        return image_url
    else:
        return None

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    print('Servers (guilds) the bot is a member of:')
    
    for guild in bot.guilds:
        print(f'{guild.name} (ID: {guild.id})')

    user_id = 146187721252143104
    user = bot.get_user(user_id)
    if user:
        try:
            await user.send(f'Bot is now online!')
            print(f'Sent online alert to {user.name} ({user.id})')
        except discord.errors.Forbidden:
            print("Couldn't send DM. The user might have DMs disabled or blocked the bot.")


@bot.event
async def on_guild_join(guild):
    target_server_id = 1105019092332724224  # Replace with the ID of the target server (Server Y)
    target_channel_id = 1105019093532291154  # Replace with the ID of the target channel in the target server

    if guild.id != target_server_id:
        return  # Only send the alert to the target server

    target_channel = bot.get_channel(target_channel_id)
    if target_channel:
        try:
            await target_channel.send(f'Pascual joined the server: {guild.name} (ID: {guild.id})')
            print(f'Sent add alert to target channel in target server!')
        except discord.errors.Forbidden:
            print("Alert couldn't be sent...")




@bot.event
async def on_guild_join(guild):
    user_id = 146187721252143104
    user = bot.get_user(user_id)
    guild_id = 1105019092332724224
    guild = bot.get_guild(guild_id)
    if guild_id == bot.get_guild(guild_id):
        target_channel = bot.get_channel(1105019093532291154)
        if target_channel:
            try:
                await target_channel.send(f'Pascual joined the server: {guild.name} (ID: {guild.id})')
                print(f'Sent alert to main server!')
            except discord.errors.Forbidden:
                print("Alert couldn't be sent...")

    if user:
        try:
            await user.send(f'Pascual joined the server: {guild.name} (ID: {guild.id})')
            print(f'Sent add alert to {user.name} ({user.id})')
        except discord.errors.Forbidden:
            print("Couldn't send DM. The user might have DMs disabled or blocked the bot.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    

    if message.author.id in close:
        if 'kodol' in message.content.lower():
            response = 'mi mamita hermosa bonita'
            await message.channel.send(response)
            print(f"Message content: {message.content}")
            print(f"Author ID: {message.author.id}")

        elif 'kasueler' in message.content.lower():
            response = 'fokiu father .l.'
            await message.channel.send(response)

    elif 'pascual' in message.content.lower():
        keyword = "siamese cat"  # Replace with the keyword for the image
        image_url = get_unsplash_image(keyword)
        
        if image_url:
            await message.channel.send(image_url)
        else:
            await message.channel.send('Cagó la API')

    elif 'yelo' in message.content.lower():
        user_id = 146361216044892160  # Mention the user who sent the message
        custom_emoji = '<:hoal:1138915980727296181>'  # Replace with your custom emoji
        response = f"<@{user_id}> {custom_emoji}{custom_emoji}{custom_emoji}"
        await message.channel.send(response)
    
    elif 'panda' in message.content.lower():
        user_id = 345694254649180161  # Mention the user who sent the message
        custom_emoji = '<:floppy:1138916037887275178>'  # Replace with your custom emoji
        response = f"<@{user_id}> chupalo panda {custom_emoji}"
        await message.channel.send(response)

    elif 'akemi' in message.content.lower():
        print(f"Message content: {message.content}")
        print(f"Author ID: {message.author.id}")
        user_id = 699079977748135936
        await message.channel.send(f"<@{user_id}> que te follen")

    await bot.process_commands(message)


if __name__ == '__main__':
    bot.run(TOKEN)
