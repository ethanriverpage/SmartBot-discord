import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import bot_database.bot_database as db

load_dotenv
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

print(f"Logging in with Discord token {TOKEN}")

Bot = commands.Bot(intents=intents,command_prefix='~')

@Bot.event
async def on_ready():
    print(f"We have logged in as {Bot.user}")

def botecho():
    @Bot.command()
    async def echo(ctx, arg):
        await ctx.send(arg)

def user_register():
    @Bot.command()
    async def register(ctx, lastfm_user):
        db.adduser({ctx.message.author.id}, {lastfm_user}, {ctx.message.author})
        print("Added user")
        await ctx.send(f"Registered user {ctx.message.author} to Last.fm user {lastfm_user}!")

botecho()
user_register()

Bot.run(TOKEN)