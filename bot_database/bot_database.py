import os
import sqlite3
from dotenv import load_dotenv

load_dotenv

cx = sqlite3.connect('users.db')
cu = cx.cursor()

def createdb():
    cu.execute("CREATE TABLE IF NOT EXISTS users(discord_id INTEGER PRIMARY KEY, lastfm_user TEXT, discord_user TEXT")
    print("Created database 'users'")
    cu.execute("INSERT INTO users VALUES (1, 'testlastfmuser', 'testuser')")
    print("Added test user")

def adduser(discord_id, lastfm_user, discord_user):
    cu.execute(f"INSERT INTO users VALUES ({discord_id}, '{lastfm_user}', '{discord_user}")
    print(f"Added user {discord_user} with Discord ID {discord_id} and Last.fm user {lastfm_user} to the database")

def printusers():
    cu.execute("SELECT * FROM users")
    results = cu.fetchall()
    print(results)