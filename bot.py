import discord
import os
import random
import requests
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import app_commands
from functions import process_message
from cogs.custom_help import custom_help
from db.keyword_db import load_keyword_responses, update_keyword_response, remove_keyword
from db.database import get_pool

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("DISCORD_TOKEN is not set in environment variables. Check your .env file.")

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
if UNSPLASH_ACCESS_KEY is None:
    raise ValueError("UNSPLASH_ACCESS_KEY is not set in environment variables. Check your .env file.")

OPENAI_KEY = os.getenv("OPENAI_KEY")
if OPENAI_KEY is None:
    raise ValueError("OPENAI_KEY is not set in environment variables. Check your .env file.")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.dm_messages = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!pi', intents=intents)
bot.remove_command('help')

owner_id = 146187721252143104
close = [710679721859612682]

def get_unsplash_image(keyword):
    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    url = f"https://api.unsplash.com/photos/random?query={keyword}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["urls"]["regular"]
    return None

def get_waifu(keyword):
    url = f"https://api.waifu.pics/sfw/{keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["url"]
    return None

@bot.command(name="help")
async def help(ctx):
    await custom_help(ctx)

@bot.event
async def on_ready():
    bot.pool = await get_pool()
    bot.keyword_responses = await load_keyword_responses(bot.pool)
    try:
        # Forzar sincronización solo en tu servidor
        GUILD_ID = discord.Object(id=1105019092332724224)
        synced = await bot.tree.sync(guild=GUILD_ID)
        print(f"Synced {len(synced)} command(s) to the test guild.")
    except Exception as e:
        print("Error syncing commands:", e)
    print(f'We have logged in as {bot.user}\n')
    for guild in bot.guilds:
        print(f'{guild.name} (ID: {guild.id})')
    main_guild_id = 1105019092332724224
    alert_channel_id = 1138923031989866596
    main_guild = bot.get_guild(main_guild_id)
    alert_channel = main_guild.get_channel(alert_channel_id)
    if alert_channel:
        try:
            await alert_channel.send(f'Bot is now online!')
            print(f'Sent online alert to {alert_channel.name} on {main_guild.name}')
        except discord.errors.Forbidden:
            print("Couldn't send alert message.")

@bot.event
async def on_guild_join(guild):
    main_guild_id = 1105019092332724224
    alert_channel_id = 1138923031989866596
    main_guild = bot.get_guild(main_guild_id)
    alert_channel = main_guild.get_channel(alert_channel_id)
    if alert_channel:
        await alert_channel.send(f'Pascual joined a new server: {guild.name} (ID: {guild.id})')

@bot.command(name="say", help="Make pascual say something")
async def say(ctx, *, prompt: str):
    await ctx.message.delete()
    await ctx.send(prompt)

@bot.tree.command(name="get_image", description="Get an image based on the keyword you give.")
async def get_image(interaction: discord.Interaction, *, prompt: str):
    image_url = get_unsplash_image(prompt)
    if image_url:
        embed = discord.Embed(title=f"Result for: `{prompt}`", color=discord.Color.pink())
        embed.set_image(url=image_url)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(f"No images found for keyword: `{prompt}`")

@bot.command(name='emoteid')
async def emoteid(ctx, emoji: str):
    # Buscar coincidencias con formato <a:name:id> o <:name:id>
    import re
    match = re.match(r'<(a?):(\w+):(\d+)>', emoji)
    if match:
        is_animated = bool(match.group(1))
        name = match.group(2)
        emote_id = match.group(3)
        await ctx.send(f"🆔 ID del emoji `{name}`: `{emote_id}` {'(animado)' if is_animated else ''}")
    else:
        await ctx.send("❌ Ese no parece ser un emoji personalizado del servidor.")

@bot.command(name="wa", help="Enter a keyword to get a waifu of your liking!")
async def wa(ctx, prompt: str):
    image_url = get_waifu("waifu")
    if image_url:
        embed = discord.Embed(title="Here's your `waifu`", color=discord.Color.pink())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('no funkó XD')

@bot.command(name="list_keywords", help="List all keywords registered in the bot.")
async def list_keywords(ctx):
    if not hasattr(bot, "keyword_responses"):
        await ctx.send("Las keywords aún no están cargadas.")
        return

    if not bot.keyword_responses:
        await ctx.send("No hay keywords registradas.")
        return

    # Obtener la lista de keywords
    keywords = list(bot.keyword_responses.keys())
    keywords.sort()

    # Discord tiene límite de caracteres por mensaje (2000), así que dividimos si es necesario
    chunk_size = 50
    chunks = [keywords[i:i + chunk_size] for i in range(0, len(keywords), chunk_size)]

    for chunk in chunks:
        formatted = "\n".join(f"- `{k}`" for k in chunk)
        embed = discord.Embed(
            title="📚 Lista de Keywords",
            description=formatted,
            color=discord.Color.pink()
        )
        await ctx.send(embed=embed)


@bot.command(name="pascual", help="Get a random siamese cat image")
async def pascual(ctx):
    image_url = get_unsplash_image("siamese cat")
    if image_url:
        embed = discord.Embed(color=discord.Color.pink())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Cagó la API')

@bot.tree.command(name="helo", description="paskualin te saluda, ke mejor")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"henlo {interaction.user.mention}!", ephemeral=True)

@bot.tree.command(name="rolley", description="Roll a number between 0 and 100")
async def roll(interaction: discord.Interaction, limit: int = 100):
    if limit <= 0:
        await interaction.response.send_message("Invalid limit provided.")
        return
    rolled_number = random.randint(0, limit)
    embed = discord.Embed(description=f"{interaction.user.mention} rolls {rolled_number} points <:Ok:1151179767555563541>", color=discord.Color.pink())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="add_kw", description="Add or update a keyword response")
async def add_keyword_slash(interaction: discord.Interaction, keyword: str, user_id: str, random_flag: int, response_type: str = "text", *, response_content: str):
    if interaction.user.id != owner_id:
        await interaction.response.send_message("Only the owner can use this command.", ephemeral=True)
        return

    user_id = int(user_id)
    random_flag = random_flag == 1

    data = {
        "user_id": user_id,
        "random": random_flag,
        "type": response_type,
        "content": response_content if response_type == 'text' else None,
        "emoji": response_content if response_type == 'emoji' else None,
        "gif_url": response_content if response_type == 'gif' else None,
        "responses": [response_content] if random_flag else [],
    }

    await update_keyword_response(bot.pool, keyword, data)
    bot.keyword_responses = await load_keyword_responses(bot.pool)

    embed = discord.Embed(title=f"Added/updated the `{keyword}` keyword response!",
                          description=f"User ID: {user_id}\nRandom: {random_flag}\nType: {response_type}\nContent: {response_content}",
                          color=discord.Color.pink())
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="remove_kw", description="Remove a keyword from the dictionary.")
async def remove_keyword_slash(interaction: discord.Interaction, keyword: str):
    if interaction.user.id != owner_id:
        await interaction.response.send_message("Only the owner can use this command.", ephemeral=True)
        return

    await remove_keyword(bot.pool, keyword)
    bot.keyword_responses = await load_keyword_responses(bot.pool)

    embed = discord.Embed(title=f"Keyword `{keyword}` has been removed.", color=discord.Color.pink())
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    if not hasattr(bot, "keyword_responses"):
        print("keyword_responses not loaded yet.")
        return

    await process_message(message, bot.keyword_responses, bot)

if __name__ == '__main__':
    bot.run(TOKEN)
