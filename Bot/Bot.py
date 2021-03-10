
import discord 
import json
import os
import importlib.util
import asyncio
import requests

async def status(Client):
    import asyncio
    while True:
        #x = requests.post("https://top.gg/api//bots/810478441224732702/stats", data = json.dumps({
            #"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgxMDQ3ODQ0MTIyNDczMjcwMiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE1MzcxNTcwfQ.vb0pnlkBUVW_JllUPUIazki25BF8eakvMdTlJ4kDqo8",
            #"server_count": len(list(Client.guilds))
        #}), headers={'content-type': 'application/json'})
        #print(x.status_code)
        #try:
            #print(x.text)
        #except:
            #pass
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