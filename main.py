import discord
from discord.ext import commands
import os
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)

@bot.event
async def on_ready():
    print('GHC Esports Discord Bot is ready to go!')

#Loads Cog Files
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

#Reloads Cog Files
@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    print('Commands have been reloaded')

#Unloads Cog Files
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run('NzgzODYyODQ3MzU1NjE3MzAw.X8g7Kg.2-VQ6Wbjn6MiFV_BGfBA0oeB2SQ')