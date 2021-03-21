
# Made by GodOf_Lua

from Modules.DataManagement import *
from Modules.Discord.Embeds import *
from Modules.Discord.Author import *
from Modules.Discord.Prompts import *
from Modules.Discord.RankRange import *
from Modules.Discord.Roles import *
from Modules.RandomGenerators.generateCode import *
from discord.utils import get
import discord
import json
import requests

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

def groupexist(serverid,groupid):
    network = requests.get("https://groups.roblox.com/v1/groups/"+groupid)
    if network.status_code == 200:
        return json.loads(network.text)
    else:
        return "unavailable"

def valCookie(cookie):
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        network = requests.get("https://api.roblox.com/currency/balance", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        return network.status_code
    else:
        return "Unable to fetch X_CSRF_TOKEN"

async def run(message, Arguments, *args):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId]",
            "command": "valcookie",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    GroupId = Arguments[1]

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.administrator

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`ADMINISTRATOR`"
        })
        return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    mainMsg = await throw("workingMethod", message.channel.send)

    if not GroupId in GuildData["BOUND_GROUPS"]:
        await mainMsg.edit(embed=discord.Embed(
            title = "Missing records",
            description = "This group wasn't bound yet or has set a cookie. Call !setcookie or !bind to fix that.",
            color = 0xc84c4c
        ))
        return
    
    if not "COOKIE" in GuildData["BOUND_GROUPS"][GroupId]:
        await mainMsg.edit(embed=discord.Embed(
            title = "Missing records",
            description = "There was no cookie set yet to this group. Call !setcookie to fix that.",
            color = 0xc84c4c
        ))
        return

    ret = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])
    if ret == 200:
        await mainMsg.edit(embed=discord.Embed(
            title = "Valid cookie",
            description = "This cookie is valid.",
            color = 0x3a9518
        ))
    else:
        await mainMsg.edit(embed=discord.Embed(
            title = "Invalid cookie or api error.",
            description = "This cookie is invalid or an API error occoured.",
            color = 0xc84c4c
        ))
