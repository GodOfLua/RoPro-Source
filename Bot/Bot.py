
import discord 
import json
import os
import importlib.util
import asyncio

async def status(Client):
    import asyncio
    while True:
        await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" ! | !invite"))
        await asyncio.sleep(20)
        totalCount = 0
        for i in Client.guilds:
            totalCount += len(i.members)
        await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" over "+str(totalCount)+" users"))
        await asyncio.sleep(20)

class Bot():

    def Token(self,TestMode):
        Settings = json.loads(open("./Data/BOT_SETTINGS.json").read())
        Token = Settings["TOKEN"]

        if TestMode:
            Token = "NzA3NTkyNzkxMjI3NjI5NjQy.XrLDIw.vCAYlAw9t1ku8emJ_0IfhVWejfg"
        return Token 

    def Client(self):
        intents = discord.Intents.default()
        intents.members = True
        return discord.Client(intents=intents)