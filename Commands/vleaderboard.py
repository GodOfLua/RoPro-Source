
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
from Modules.Discord.Author import *
from Modules.Discord.Prompts import *
import secrets
from datetime import datetime
import time

def GetUserEconomyData(id):
    AuthorData = getData(f"./Data/UserEconomy_Data/{str(id)}.json")
    if AuthorData == None:
        DefaultData = {
            "cashvalue" : {
                "wallet" : 0,
                "bank" : 0
            },
            "inventory" : {},
            "lastVote": 0,
        }
        SaveData(f"./Data/UserEconomy_Data/{str(id)}.json",DefaultData)
        AuthorData = getData(f"./Data/UserEconomy_Data/{str(id)}.json")
    return AuthorData

async def run(message, Arguments, Client, Discord_Bot):

    gen = ""

    with open("./Leaderboards/Votes.json", "r") as file:
        data = json.loads(file.read())
        file.close()

    page = 1
    try:
        Arguments[1]
        if Arguments[1].isnumeric():
            page = int(Arguments[1])
    except:
        pass

    if len(data["votes"]) >= 14*(page-1)+1:
        for i in range(14*page):
            try:
                data["votes"][i]
                gen = gen +"\n"+str(i+1)+". "+data["votes"][i]["name"]+ " **-** " + str(data["votes"][i]["votes"]) + " votes"
            except:
                pass 
    else:
        gen = "Nothing to see here!"
    
    embed = discord.Embed(
        title = "Global vote leaderboard",
        description = gen,
        color = 0xc337ac,
    )
    embed.set_footer(text="Page "+str(page)+"; run !vlb "+str(page+1)+" to see the next page. | Refreshes every 15 seconds | Powered by RoPro System · !invite")

    await message.channel.send(embed=embed)