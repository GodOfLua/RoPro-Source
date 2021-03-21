
# Made by GodOf_Lua

# Get All Modules
# pylint: disable=no-member

from Modules.DataManagement import *
from Modules.Discord.Embeds import *
from Modules.Discord.Author import *
from Modules.Discord.Prompts import *
from Modules.Discord.RankRange import *
from Modules.Discord.Roles import *
from Modules.Discord.Channel import *
from Modules.RandomGenerators.generateCode import *
from discord.utils import get
import discord
import requests

async def run(message, Arguments, Client, Discord_Bot):

    if len(Arguments) < 4:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId] [RankRange] [RoleMention | RoleId | RoleName]",
            "command": "bind",
            "length": 3,
            "pronounce": "Arguments"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    SpecifiedGuildData = GuildData

    GroupId = Arguments[1]
    RankRange = getRankRange(Arguments[2])
    Role = getRole(message.content[0+len(Arguments[0])+2+len(Arguments[1])+1+len(Arguments[2]):len(message.content)], message.guild.roles, message)

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })
        return

    if not Role:
        await throw("roleError", ReplyMethod)
        return

    if not RankRange:
        await throw("rankRangeError", ReplyMethod)
        return

    if not GroupId in SpecifiedGuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData = GuildData

    SpecifiedGuildData["BOUND_GROUPS"][GroupId]["BINDING"].append({
        "roleId": Role.id,
        "min": RankRange["min"],
        "max": RankRange["max"]
    })
    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    GuildData = SpecifiedGuildData
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    await message.channel.send(embed=discord.Embed(
        description = "Bind has been added.",
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))
