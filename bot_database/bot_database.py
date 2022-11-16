import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

cx = sqlite3.connect('./bot_database/users.db')
cu = cx.cursor()

def createdb():
    cu.execute("CREATE TABLE IF NOT EXISTS users(discord_id INTEGER PRIMARY KEY, spotify_user TEXT, discord_user TEXT)")
    print("Created database 'users'")
#    cu.execute("INSERT INTO users VALUES (1, 'testspotifyuser', 'testuser')")
#    print("Added test user")
    return 0

def checkuser(discord_id):
    cu.execute(f"SELECT EXISTS(SELECT discord_id FROM users WHERE discord_id=?)", (discord_id,))
    checkeduser = cu.fetchone()[0]
    print(checkeduser)
    return(checkeduser)

def adduser(discord_id, spotify_user, discord_user):
    cu.execute(f"INSERT OR REPLACE INTO users VALUES ({discord_id}, '{spotify_user}', '{discord_user}')")
    print(f"Added user {discord_user} with Discord ID {discord_id} and Spotify user {spotify_user} to the database")
    cx.commit()

def printusers():
    cu.execute("SELECT * FROM users")
    results = cu.fetchall()
    return results

def retrievespotifyuser(discord_id):
    cu.execute("SELECT spotify_user FROM users WHERE discord_id=?", (discord_id,))
    spotify_user_result = cu.fetchone()[0]
    print(spotify_user_result)
    return spotify_user_result
