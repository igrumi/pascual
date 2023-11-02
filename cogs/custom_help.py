import discord
from discord.ext import commands

async def custom_help(ctx):
    # Create an embed for the help message
    embed = discord.Embed(title="Bot Commands", color=discord.Color.pink())

    # Iterate through the bot's commands and add them to the embed
    for command in ctx.bot.commands:
        if command.name != 'help':
            embed.add_field(name=f"!!{command.name}", value=command.help, inline=False)
            embed.set_footer(text="\n\nAlso check the slash commands with '/' !")

    await ctx.send(embed=embed)

