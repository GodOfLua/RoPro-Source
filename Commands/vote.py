
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

    AuthorData = GetUserEconomyData(message.author.id)

    if "lastVote" in AuthorData:
        if round(time.time()-AuthorData["lastVote"], 2) < 43200 and message.author.id != 311222306695544833:
            await message.channel.send(embed=discord.Embed(
                description = "You already voted for the bot before "+str(round(time.time() - AuthorData["lastVote"], 2)) + " seconds. You can vote for the bot again in `"+str(43200-round(time.time() - AuthorData["lastVote"], 2))+"s`",
                color = 0xc84c4c
            ))
            return

    money = 1000
    votes = 1

    if datetime.today().weekday() >= 5:
        money = 2500
        votes = 2

    msg = await executePrompt(Client, message.channel.send, discord.Embed(
        description = f"Click [here](https://top.gg/bot/810478441224732702/vote) to vote for our bot.\nDoing so will reward you ${money} in our economy system. (You get $2500 for voting on weekends)\nSay `done` once you voted.\nPrompt will expire in 600 seconds.",
        color = 0x8000ff
    ), message, 600, "done")

    if msg == "cancel" or msg == "timeout":
        await throw(msg, message.channel.send)
        return 

    res = requests.get(f"https://top.gg/api//bots/810478441224732702/check?userId="+str(message.author.id), headers={
        "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgxMDQ3ODQ0MTIyNDczMjcwMiIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE1MzcxNTcwfQ.vb0pnlkBUVW_JllUPUIazki25BF8eakvMdTlJ4kDqo8"
    })

    if res.status_code != 200:
        await message.channel.send(embed=discord.Embed(
            description = "API error, try again later.",
            color = 0xc84c4c
        ))
        return 

    res = json.loads(res.text)

    if res["voted"] > 0:

        AuthorData = GetUserEconomyData(message.author.id)
        AuthorData["cashvalue"]["wallet"] += money
        AuthorData["lastVote"] = time.time()
        SaveData(f"./Data/UserEconomy_Data/{str(message.author.id)}.json",AuthorData)
        x = secrets.token_hex(16)

        with open(f"./Caching/Votes/{x}.json", "a+") as file:
            file.write(json.dumps({
                "name": message.author.name,
                "id": str(message.author.id),
                "votes": votes
            }))
            file.close()

        await message.channel.send(embed=discord.Embed(
            description = f"Thanks for voting for our bot! ${money} has been added to your wallet.\nThe vote leaderboard gets refreshed every 15 seconds.",
            color = 0x3a9518
        ))