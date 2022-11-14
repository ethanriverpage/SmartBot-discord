import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import bot_database.bot_database as db

#Load .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
#Set Discord bot intents
intents = discord.Intents.default()
intents.message_content = True

print(f"Logging in with Discord token {TOKEN}")
#Bot login
Bot = commands.Bot(intents=intents,command_prefix='~')
@Bot.event
async def on_ready():
    print(f"We have logged in as {Bot.user}")

#Database initalization
dbexists = os.path.exists('./bot_database/users.db')
if dbexists == False:
    print("Database does not exists, creating now")
    db.createdb()
elif dbexists == True:
    print("Database already exists! Continuing.")
else:
    raise TypeError("What")

#Bot commands
def user_echo(): #Simple echo command issued with ~echo
    @Bot.command()
    async def echo(ctx, arg):
        await ctx.send(arg)

def user_register(): #Registers user into SQLite database, ~register lastfm_username
    @Bot.command()
    async def register(ctx, lastfm_user):
        discord_user = ctx.message.author
        discord_id = ctx.message.author.id
        print("DEBUG" + str(discord_id) + str(lastfm_user) + str(discord_user))
        usercheck = bool(db.checkuser(discord_id))
        if usercheck == 1:
            db.adduser(discord_id, lastfm_user, discord_user)
            await ctx.send("Registered user!")
        elif usercheck == 0:
            await ctx.send("User already exists!")
        else:
            print("Error. Continuing...")

def user_printusers(): #Prints out database, split by list, ~printusers
    @Bot.command()
    async def printusers(ctx):
        userlist = db.printusers()
        res = '\n'.join([str(item) for item in userlist])
        if res == "":
            await ctx.send("No users!")
        else:
            await ctx.send(res)
        
user_printusers()
user_echo()
user_register()

Bot.run(TOKEN)