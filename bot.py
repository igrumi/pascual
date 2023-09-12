import discord
import os
import random
import aiohttp
import requests
import wavelink
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

#Loads up the environment variables from .env file
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Enable guild (server) join and leave events
intents.members = True  # Enable member-related events
intents.dm_messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

#Close people list for certain commands
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


#on_ready event XD!
@bot.event
async def on_ready():
  try:
      synced = await bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

  print(f'We have logged in as {bot.user}\n')
  print('Servers (guilds) the bot is a member of:')
  for guild in bot.guilds:
    print(f'{guild.name} (ID: {guild.id})')

  user_id = 146187721252143104
  user = bot.get_user(user_id)

  if user:
    try:
      await user.send(f'Bot is now online!')
      print(f'\nSent online alert to {user.name} ({user.id})')
    except discord.errors.Forbidden:
      print(
        "Couldn't send DM. The user might have DMs disabled or blocked the bot."
      )

@bot.event
async def on_guild_join(guild):
    print(f'Bot has joined the guild: {guild.name} (ID: {guild.id})')
    main_guild_id = 1105019092332724224
    alert_channel_id = 1138923031989866596

    main_guild = bot.get_guild(main_guild_id)
    alert_channel = main_guild.get_channel(alert_channel_id)

    if alert_channel is not None:
        await alert_channel.send(f'Pascual joined a new server: {guild.name} (ID: {guild.id})')
    else:
        print('Alert channel not found in the main guild.')

@bot.tree.command(name="ola", description="paskualin te saluda, ke mejor")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"hey {interaction.user.mention}!", ephemeral= True)

@bot.tree.command(name="roll", description="Roll a number between 0 and 100")
async def roll(interaction: discord.Interaction, limit: int = 100):
    ok_emoji = "<:Ok:1151179767555563541>"
    user = interaction.user.name
    if limit <= 0:
        await interaction.response.send_message("Invalid limit provided.")
        return
    
    rolled_number = random.randint(0, limit)
    embed = discord.Embed(description= f"{interaction.user.mention} rolls {rolled_number} points {ok_emoji}",
                          color=discord.Color.pink())

    await interaction.response.send_message(embed=embed)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.author.id in close:
    if 'kodol' in message.content.lower():
      print(f"Message content: {message.content}")
      print(f"Author ID: {message.author.id}")
      user_id = os.getenv("KODOL")
      gif = 'https://tenor.com/view/siamese-cat-siamese-cutecats-kitten-kitty-gif-24959894'
      responses = [
        f'<@{user_id}> mi mamita hermosa bonita',
        f'<@{user_id}> fokiu mother .l.',
        f'<@{user_id}> mira mother literalmente yo {gif} '
      ]
      random_response = random.choice(responses)
      await message.channel.send(random_response)

    elif 'kasueler' in message.content.lower():
      response = 'fokiu father .l.'
      await message.channel.send(response)

  if 'pascual' in message.content.lower():
    keyword = "siamese cat"  # Replace with the keyword for the image
    image_url = get_unsplash_image(keyword)

    if image_url:
      await message.channel.send(image_url)
    else:
      await message.channel.send('Cagó la API')

  if 'yelo' in message.content.lower():
    user_id = 146361216044892160  # Mention the user who sent the message
    custom_emoji = '<:hoal:1138915980727296181>'  # Replace with your custom emoji
    response = f"<@{user_id}> {custom_emoji}{custom_emoji}{custom_emoji}"
    await message.channel.send(response)

  if 'panda' in message.content.lower():
    user_id = 345694254649180161  # Mention the user who sent the message
    custom_emoji = '<:floppy:1138916037887275178>'  # Replace with your custom emoji
    response = f"<@{user_id}> chupalo panda {custom_emoji}"
    await message.channel.send(response)

  if 'neicho' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 435217891579920386
    await message.channel.send(f"<@{user_id}> deranker desgraciao")

  if 'bichota' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 529061870553006084
    await message.channel.send(f"<@{user_id}> WOOTINISTA")

  if 'vintage' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 549235628332810261
    if user_id:
      await message.channel.send(f"<@{user_id}> merami")
    else:
      await message.channel.send(f"{user_id} not found!")

  if 'bufos' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 969009500583505950
    await message.channel.send(f"<@{user_id}>")
    await message.channel.send(
      f"https://tenor.com/view/ferret-bath-gif-18303106")

  if 'akemi' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 699079977748135936
    await message.channel.send(f"<@{user_id}> que te follen ijo deperra")

  if 'daqo' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 209051034318929920
    await message.channel.send(f"<@{user_id}> que te follen")

  if 'pupi' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    custom_emoji = '<:floppy:1138916037887275178>'
    user_id = 158009300092977153
    await message.channel.send(f"<@{user_id}> {custom_emoji}")
    await message.channel.send(f"{custom_emoji}")
    await message.channel.send(f"{custom_emoji}")
    await message.channel.send(f"{custom_emoji}")
    await message.channel.send(f"{custom_emoji}")

  if 'neicho' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 435217891579920386
    await message.channel.send(f"<@{user_id}> que te follen")

  if 'nesumi' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 774506123696144444
    await message.channel.send(f"<@{user_id}> que te follen")

  if 'xeb' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 415593324083150848
    await message.channel.send(f"<@{user_id}> que te follen")

  if 'pogon' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 814643903709446184
    await message.channel.send(f"<@{user_id}> que te follen")

  if 'makipro' in message.content.lower():
    print(f"Message content: {message.content}")
    print(f"Author ID: {message.author.id}")
    user_id = 541049717870821425
    await message.channel.send(f"<@{user_id}> que te follen")

  await bot.process_commands(message)

if __name__ == '__main__':
  bot.run(TOKEN)
