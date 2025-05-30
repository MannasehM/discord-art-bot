import discord
from discord.ext import commands
# print(discord.__file__)
# print(dir(discord))
# print(hasattr(discord, 'Bot'))
import os
from dotenv import load_dotenv
from met_api import get_random_artwork

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Creates an Intents object using the default settings
intents = discord.Intents.default()
# Allows bot to read actual text messages
intents.message_content = True
intents.members = True
# Creates bot and telling it which events it's allowed to see
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    print("-------")

@bot.command(name="art", description="Get a random artwork from the MET Museum")
async def art(ctx):
    max_retries = 5
    for attempt in range(max_retries):
        art = get_random_artwork()
        if art["image"]:
            embed = discord.Embed(
                title=art["title"], 
                url=art["url"], 
                description=f"Artist: {art['artist']}\nDate: {art['date']}"
            )
            embed.set_image(url=art["image"])
            await ctx.send(embed=embed)
            return
    # If no image found after retries:
    await ctx.send("Sorry, I couldn’t find any artwork images after several tries. Please try again later!")

# Starts Discord Bot, and stays running for event/command listening
bot.run(TOKEN)