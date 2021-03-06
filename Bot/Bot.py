
import discord 
import json

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

def intialize(IsTest):
    intents = discord.Intents.default()
    intents.members = True

    Settings = json.loads(open("./Data/BOT_SETTINGS.json").read())
    Token = Settings["TOKEN"]

    if IsTest:
        Token = "NzA3NTkyNzkxMjI3NjI5NjQy.XrLDIw.vCAYlAw9t1ku8emJ_0IfhVWejfg"
    return discord.Client(intents=intents), Token