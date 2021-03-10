
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *

async def run(message, Arguments, Client, Discord_Bot):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<GroupId>",
            "command": "shout",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not Arguments[1].isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    res = requests.get("https://groups.roblox.com/v1/groups/"+Arguments[1])

    if res.status_code == 400:
        await message.channel.send(embed=discord.Embed(
            description = "Invalid group id.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0xc84c4c
        ))
    elif res.status_code == 200:
        res = json.loads(res.text)
        if res["shout"] == None:
            print("yes")
            await message.channel.send(embed=discord.Embed(
                description = "The group's shout is empty.\nPlease note this command is very unreliable due to the behavior of the roblox API.",
                footer = "Powered by RoPro Verification System · !invite",
                color = 0xc84c4c
            ))
            return
        await message.channel.send(embed=discord.Embed(
            description = "'"+res["shout"]["body"]+"' by "+res["shout"]["poster"]["username"]+"\nPlease note this command is very unreliable due to the behavior of the roblox API.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0xc84c4c
        ))
    else:
        await throw("apiError", ReplyMethod)