
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
            "arguments": "<GroupId> <Username>",
            "command": "exile",
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
        return

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

    user = Arguments[2]

    userResponse = requests.get("http://api.roblox.com/users/get-by-username?username="+user)

    if userResponse.status_code == 200:
        userResponse = json.loads(userResponse.text)
        if not "Id" in userResponse:
            embed.description = "User dosen't exist."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
        Username = userResponse["Id"]
    else:
        await mainMSG.edit(embed=apiError())
        return

    res = requests.delete(f"https://groups.roblox.com/v1/groups/{GroupId}/users/{Username}", headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]})

    if res.status_code == 400:
        embed.description = "API error or user not in group."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return
    elif res.status_code == 403:
        embed.description = "Unable to kick user. User role is higher than bot role."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return
    elif res.status_code == 200:
        embed.description = "User has been exiled from group."
        embed.color = 0xc337ac
        await mainMSG.edit(embed=embed)
        return
    else:
        await mainMSG.edit(embed=apiError())
        return