
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


async def run(message, Arguments, Client, Discord_Bot):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId]",
            "command": "setcookie",
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
    Role = Discord_Bot.hasModRole(message.author, message.guild)
    RoleId = Role[1]
    HasRole = Role[0]
    role = Role[2]

    if RoleId == 0:
        if not Admin:
            await throw("permissionError", {
                "method": message.channel.send,
                "permission": "`ADMINISTRATOR`"
            })
            return
    else:
        if not HasRole:
            await throw("roleError2", {
                "method": message.channel.send,
                "permission": role.mention
            })
            return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    SpecifiedGuildData = GuildData

    await throw("checkDM", ReplyMethod)

    dm = await getDM(Author)

    msg = await executePromptDM(Client, dm.send, discord.Embed(
        title = "Set the bot cookie of your roblox group", 
        description = "Please respond with the .ROBLOSECURITY cookie of your bot account. (Make sure to make an seperate one) The cookie is required to login into the account and perform rank changes so commands such as promote are able to work. If you don't know how to get the cookie please click [here](https://www.youtube.com/watch?v=KIMT82TLS9I)\nThe prompt will expire in 300 seconds.",
        color = 0xc337ac,
    ), message, 300)

    if msg == "cancel" or msg == "timeout":
        await throw(msg, dm)
        return 

    if not GroupId in SpecifiedGuildData["BOUND_GROUPS"]:
        SpecifiedGuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", SpecifiedGuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData = GuildData


    SpecifiedGuildData["BOUND_GROUPS"][GroupId]["COOKIE"] = msg.content
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", SpecifiedGuildData)
    await dm.send(embed=discord.Embed(
        description = "Cookie of your group has been successfully added/updated",
        color = 0x3a9518
    ))
