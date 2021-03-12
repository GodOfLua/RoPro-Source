
# Import Modules

import discord 
import json
import os
import importlib.util
import asyncio
import requests
import time
from Modules.DataManagement import *
from discord import Embed

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

    async def procressCooldown(self, userId, command, Reply):
        if str(userId) in self.cooldown and not command in self.ignoreCooldown:
            Difference = round(time.time() - self.cooldown[str(userId)],2)
            if Difference < 1:
                return False
            if Difference <= 3:
                await Reply(embed=Embed(
                    title = "Command Cooldown",
                    description = "You are currently on command cooldown. Time remaining: `"+str(round(3-Difference,2))+"`secs",
                    color = 0xff0000
                ))
                return False 
            else:
                self.cooldown[str(userId)] = time.time()
                return True
        else:
            self.cooldown[str(userId)] = time.time()
            return True

    async def procressCommands(self, message, Arguments, Command, Client, Discord_Bot):

        try:
            spec = importlib.util.spec_from_file_location("module.name", f"./Commands/{Command}.py")
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            await foo.run(message, Arguments, Client, Discord_Bot)
        except OSError as e:
            return 
        except Exception as e:
            raise Exception(e)

    def catchGuildSettings(self, GuildId):
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

        if not "Acronyms" in GuildData:
            putAcronyms(GuildId)
            GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

        if not "RoNick" in GuildData:
            putRoNick(GuildId)
            GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
        if not "NicknameFormat" in GuildData:
            putnickformat(GuildId)
            GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

        if not "PrimaryNickname" in GuildData:
            putprimary(GuildId)
            GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

        return GuildData

    def __init__(self):
        self.cooldown = {}
        self.ignoreCooldown = []

    def addCooldownIgnore(self, array):
        for i in array:
            self.ignoreCooldown.append(i)

    def Token(self,TestMode):
        Settings = json.loads(open("./Data/BOT_SETTINGS.json").read())
        Token = Settings["TOKEN"]

        if TestMode:
            Token = "NzA3NTkyNzkxMjI3NjI5NjQy.XrLDIw.vCAYlAw9t1ku8emJ_0IfhVWejfg"
        return Token 

    def Client(self):
        intents = discord.Intents.default()
        intents.members = True
        return discord.AutoShardedClient(intents=intents)