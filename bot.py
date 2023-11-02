import discord
import os
import random
import requests
import datetime
import asyncio
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands
from functions import process_message
from cogs.custom_help import custom_help  # Import the custom_help function
from file_operations import load_keyword_responses, update_keyword_responses

#Loads up the environment variables from .env file
load_dotenv()
keyword_responses = load_keyword_responses()

TOKEN = os.getenv("DISCORD_TOKEN")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
OPENAI_KEY = os.getenv("OPENAI_KEY")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True  # Enable guild (server) join and leave events
intents.members = True  # Enable member-related events
intents.dm_messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!!', intents=intents)
bot.remove_command('help')

owner_id = 146187721252143104
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

# Fetch a random image from waifu.api using the given keyword
def get_waifu(keyword):
  url = f"https://api.waifu.pics/sfw/{keyword}"
  response = requests.get(url)
  if response.status_code == 200:
     data = response.json()
     image_url = data["url"]
     print(image_url)
     return image_url
  else:
     return None

@bot.command(name="help")
async def help(ctx):
    await custom_help(ctx)

#on_ready event XD!
@bot.event
async def on_ready():
  #daily_ping_task.start()

  try:
      synced = await bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

  print(f'We have logged in as {bot.user}\n')
  print('Servers (guilds) the bot is a member of:')
  for guild in bot.guilds:
    print(f'{guild.name} (ID: {guild.id})')


  main_guild_id = 1105019092332724224
  alert_channel_id = 1138923031989866596
  main_guild = bot.get_guild(main_guild_id)
  alert_channel = main_guild.get_channel(alert_channel_id)
  user_id = 146187721252143104
  user = bot.get_user(user_id)

  if alert_channel is not None:
    try:
      await alert_channel.send(f'Bot is now online!')
      print(f'\nSent online alert to {alert_channel.name} channel on ({main_guild.name})')
    except discord.errors.Forbidden:
      print(
        "Couldn't send DM. The user might have DMs disabled or blocked the bot."
      )

# Sends alert to the bot's main guild every time it joins a new guild
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

@bot.command(name="say", category="category_general", help="Make pascual say something")
async def say(ctx: commands.Context, *, prompt: str):
  print(f"Message sent: {ctx.message.content}")
  msg = prompt
  await ctx.message.delete()
  await ctx.send(f"{msg}")


@bot.tree.command(name="get_image", description="Get an image based on the keyword you give.")
async def get_image(interaction: discord.Interaction, *, prompt: str):
  print(f"Message sent: {prompt}")
  try:
    keyword = prompt  # Replace with the keyword for the image
    image_url = get_unsplash_image(keyword)
    print(image_url)
    if image_url:
      result_msg = f"Result for: `{keyword}`"

      embed = discord.Embed(title=result_msg, color=discord.Color.pink())
      embed.set_image(url=image_url)
      await interaction.response.send_message(embed=embed)
      #await interaction.response.send_message(f"{result_msg}" + image_url)
    else:
      await interaction.response.send_message(f"no images found for keyword: `{keyword}`")
  except Exception as e:
    # Check if you are in the server
    bot_owner = await bot.fetch_user(owner_id)
    guild = interaction.guild

    if guild and bot_owner in guild.members:
        # You are in the server, so ping you
        await interaction.response.send_message(f"<@{bot_owner.id}> An error occurred: {str(e)}")
    else:
        # You are not in the server, send a different message
        await interaction.response.send_message(f"An error occurred, DM {bot_owner.name} for help.")

@bot.command(name="wa", category="category_fun", help="Enter a keyword to get a waifu of your liking!")
async def wa(ctx: commands.Context, prompt: str):
  print(f"Message sent: {ctx.message.content}")
  keyword = prompt
  print(keyword)
  if keyword:
    keyword = "waifu"
    image_url == get_waifu(keyword)
    if image_url:
      embed= discord.Embed(title=f"Here's your `{keyword}`",color= discord.Color.pink())
      embed.set_image(url=image_url)
      await ctx.send(embed=embed)
    else:
      await ctx.send('no funkó XD')
  else:
    image_url = get_waifu(keyword)
    if image_url:
      embed= discord.Embed(title=f"Here's your `{keyword}`",color= discord.Color.pink())
      embed.set_image(url=image_url)
      await ctx.send(embed=embed)
    else:
      await ctx.send('no funkó XD')

@bot.command(name="pascual", category="category_fun", help="Get a random siamese cat image")
async def pascual(ctx: commands.Context):
  keyword = "siamese cat"  # Replace with the keyword for the image
  image_url = get_unsplash_image(keyword)

  if image_url:
    embed= discord.Embed(color= discord.Color.pink())
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)
  else:
    await ctx.send('Cagó la API')

@bot.tree.command(name="ola", description="paskualin te saluda, ke mejor")
async def hello(interaction: discord.Interaction):
  await interaction.response.send_message(f"ola {interaction.user.mention}!", ephemeral= True)

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

@bot.tree.command(name="add_keyword_slash", description="Add or update a keyword response")
async def add_keyword_slash(interaction: discord.Interaction, keyword: str, user_id: str, random_flag: int, response_type: str="text", *, response_content: str):
    if interaction.user.id != owner_id:
        await interaction.response.send_message("Only the owner can use this command.", ephemeral=True)
        return
    
    user_id = int(user_id)
    # Convert random_flag from 1 or 2 to True or False
    random_flag = random_flag == 1

    # Check if the keyword already exists in the dictionary
    if keyword in keyword_responses:
      if keyword_responses[keyword]['random']:
          # If random is True, append the response to the list
          keyword_responses[keyword]['responses'].append(response_content)
      else:
          # Update the entry as before for random=False
          keyword_responses[keyword].update({
              'user_id': user_id,
              'random': random_flag,
              'type': response_type,
              'content': response_content if response_type == 'text' else None,
              'emoji': response_content if response_type == 'emoji' else None,
              'gif_url': response_content if response_type == 'gif' else None,
              'responses': []  # Initialize an empty list for responses
          })
    else:
        # If the keyword doesn't exist, create a new entry
        keyword_responses[keyword] = {
            'user_id': user_id,
            'random': random_flag,
            'type': response_type,
            'content': response_content if response_type == 'text' else None,
            'emoji': response_content if response_type == 'emoji' else None,
            'gif_url': response_content if response_type == 'gif' else None,
            'responses': []  # Initialize an empty list for responses
        }

    # Call the update_keyword_responses function to save the changes
    update_keyword_responses(keyword_responses)

    embed = discord.Embed(title= f"Added/updated the `{keyword}` keyword response!",
                          description=f"User ID: {user_id}\n"
                                      f"Random: {random_flag}\n"
                                      f"Type: {response_type}\n"
                                      f"Content: {response_content}", 
                                      color=discord.Color.pink())
    await interaction.response.send_message(embed=embed, ephemeral=True)
    #await interaction.response.send_message(f"Keyword '{keyword}' added/updated with the following response:\n"
    #               f"User ID: {user_id}\n"
    #               f"Random: {random_flag}\n"
    #               f"Type: {response_type}\n"
    #               f"Content: {response_content}")

@bot.tree.command(name="remove_keyword", description="Remove a keyword from the dictionary.")
async def remove_keyword_slash(interaction: discord.Interaction, keyword: str):
    if interaction.user.id != owner_id:
        await interaction.response.send_message("Only the owner can use this command.", ephemeral=True)
        return
    # Check if the keyword exists in the dictionary
    if keyword in keyword_responses:
        # Remove the keyword from the dictionary
        del keyword_responses[keyword]
        # Save the updated dictionary to the JSON file
        update_keyword_responses(keyword_responses)
        embed = discord.Embed(title=f"Keyword `{keyword}` has been removed and the changes have been saved.", color= discord.Color.pink())
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(f"Keyword '{keyword}' was not found in the dictionary.", ephemeral=True)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.author.bot:
        return

  #if message.author.id in close:
  #  if 'kodol' in message.content.lower():
  #    print(f"Message content: {message.content}")
  #    print(f"Author ID: {message.author.id}")
  #    user_id = os.getenv("KODOL")
  #    gif = 'https://tenor.com/view/siamese-cat-siamese-cutecats-kitten-kitty-gif-24959894'
  #    responses = [
  #      f'<@{user_id}> mi mamita hermosa bonita',
  #      f'<@{user_id}> fokiu mother .l.',
  #      f'<@{user_id}> mira mother literalmente yo {gif} '
  #    ]
  #    random_response = random.choice(responses)
  #    await message.channel.send(random_response)

  #  elif 'kasueler' in message.content.lower():
  #    response = 'fokiu father .l.'
  #    await message.channel.send(response)

  await process_message(message, keyword_responses, bot)

#@tasks.loop(hours=24)
#async def daily_ping_task():
#    now = datetime.datetime.now()
#    # Set the time you want the bot to ping (12:00 PM)
#    target_time = now.replace(hour=12, minute=46, second=0, microsecond=0)
#    
#    if now >= target_time:
#        # Calculate the time for the next day
#        target_time += datetime.timedelta(days=1)
#    
#    # Calculate the delay until the target time
#    delay = (target_time - now).total_seconds()
#    await asyncio.sleep(delay)
    
    # Replace these user IDs with the ID of the user you want to ping
#    user_id_to_ping = 699079977748135936
    
    # Get the Discord User for the specified user ID
#    target_user = bot.get_user(user_id_to_ping)
    
#    if target_user is not None:
#        for guild in bot.guilds:
#            # Check if the target user is a member of the server
#            member = guild.get_member(target_user.id)
#            if member is not None:
#                # Get a channel where the bot has permission to send messages
#                channel = None
#                for c in guild.text_channels:
#                    if c.permissions_for(guild.me).send_messages:
#                        channel = c
#                        break
#                if channel is not None:
#                    await channel.send(f"{target_user.mention} que te follen")
#                    print(f"Daily message sent to {target_user.name}")
if __name__ == '__main__':
  bot.run(TOKEN)
