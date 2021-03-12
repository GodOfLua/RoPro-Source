
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
from Modules.Discord.Author import *
import secrets

async def run(message, Arguments, Client, Discord_Bot):

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    Admin = Author.guild_permissions.administrator

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if message.author.id != message.guild.owner.id:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`OWNER`"
        })

    with open("./WebAPI/apiKeys.json", "r") as file:
        data = json.loads(file.read())
        file.close()

    if not GuildId in data["keys"]:
        def gen():
            key = "API-KEY_"+secrets.token_hex(64)
            if key in data["used"]:
                x = gen()
                return x 
            return key 

        key = gen()

        data["keys"][GuildId] = {
            "key": key
        }
        data["used"].append(key)

        with open("./WebAPI/apiKeys.json", "w") as file:
            file.write(json.dumps(data))
            file.close()
        with open("./WebAPI/apiKeys.json", "r") as file:
            data = json.loads(file.read())
            file.close()
    
    dm = await getDM(Author)
    await throw("checkDM", ReplyMethod)
    await dm.send(embed=discord.Embed(
        description = "Your api token for this guild is: \n"+data["keys"][GuildId]["key"],
        color = 0x3a9518
    ))