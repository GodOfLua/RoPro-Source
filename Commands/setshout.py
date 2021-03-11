
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *

def get_x_csrf_token(ROBLOSECURITY):
    try:
        token_request = requests.session()
        token_request.cookies['.ROBLOSECURITY'] = ROBLOSECURITY
        r = token_request.post('https://auth.roblox.com/v2/login')
        if r.headers["X-CSRF-TOKEN"] != None:
            return r.headers["X-CSRF-TOKEN"]
        else:
            return None
    except:
        return None


def valCookie(cookie):
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        network = requests.get("https://api.roblox.com/currency/balance", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        return network.status_code
    else:
        return "Unable to fetch X_CSRF_TOKEN"

async def run(message, Arguments, Client, Discord_Bot):
    if len(Arguments) < 3:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<GroupId> <shout>",
            "command": "shout",
            "length": 2,
            "pronounce": "Arguments"
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

    Admin = Author.guild_permissions.administrator

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`ADMINISTRATOR`"
        })
        return

    mainMSG = await throw("workingMethod", ReplyMethod)

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    GroupId = Arguments[1]

    if not GroupId in GuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    verCookie = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])
    x_csrf_token = get_x_csrf_token(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])

    embed = discord.Embed()
    embed.set_footer(text="Powered by RoPro System · !invite")

    if verCookie != 200:
        embed.description = "API error or invalid cookie."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    res = requests.patch(f"https://groups.roblox.com/v1/groups/{GroupId}/status",data=json.dumps({
        "message": message.content[len(Arguments[0])+1+len(Arguments[1])+1:len(message.content)]
    }), headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]})

    if res.status_code == 200:
        embed.description = "Shout changed to: '"+message.content[len(Arguments[0])+1+len(Arguments[1])+1:len(message.content)]+"'"
        embed.color = 0xc337ac
        await mainMSG.edit(embed=embed)
    else:
        embed.description = "API error or invalid cookie."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)

