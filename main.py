import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
from met_api import get_random_artwork, get_departments, get_artworks_by_department#, search_artwork_title

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
    max_retries = 3
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

# @bot.command(name="title", help="Search for an artwork by keyword in title")
# async def search_title(ctx, *, query):
#     max_retries = 3
#     for attempt in range(max_retries):
#         art = search_artwork_title(query)
        
#         if not art: 
#             await ctx.send("No artwork found for that keyword!")
#             return
        
#         if art["image"]:
#             embed = discord.Embed(
#                 title=art["title"], 
#                 url=art["url"], 
#                 description=f"Artist: {art['artist']}\nDate: {art['date']}"
#             )
#             embed.set_image(url=art["image"])
#             await ctx.send(embed=embed)
#             return
#     # If no image found after retries:
#     await ctx.send("Sorry, I couldn’t find any artwork images after several tries. Please try again later!")

@bot.command(name="department-id", help="Get department IDs for each art department")
async def find_department_ids(ctx): 
    departments_data = get_departments()
    
    embed = discord.Embed(
        title="List of Department and Department IDs",
        description=format_department_ids(departments_data)
    )

    await ctx.send(embed=embed)

@bot.command(name="department", help="Get a random artwork from a department from an department ID")
async def department(ctx, *, department_id: int):
    max_retries = 3
    for attempt in range(max_retries):
        art = get_artworks_by_department(department_id)
        
        if not art: 
            await ctx.send("No artworks found for that department.")
            return
        
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

def format_department_ids(departments_data):
    result = ""
    for dept in departments_data: 
        id = dept["departmentId"]
        name = dept["displayName"]
        result += f"{name} - {id}\n"

    return result[:-1]

# Starts Discord Bot, and stays running for event/command listening
bot.run(TOKEN)