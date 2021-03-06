
import discord 
import json

def intialize(IsTest):
    intents = discord.Intents.default()
    intents.members = True

    Settings = json.loads(open("./Data/BOT_SETTINGS.json").read())
    Token = Settings["TOKEN"]

    if IsTest:
        Token = "NzA3NTkyNzkxMjI3NjI5NjQy.XrLDIw.vCAYlAw9t1ku8emJ_0IfhVWejfg"

    return discord.Client(intents=intents), Token