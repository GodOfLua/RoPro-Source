
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

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<StringFormat (Example: {rank} | {roname}, for more magic words view !magicwords)>",
            "command": "setnickname",
            "length": 1,
            "pronounce": "Argument"
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

    if not "NicknameFormat" in GuildData:
        putnickformat(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if len(message.content[0+len(Arguments[0])+1:len(message.content)]) < 1:
        GuildData["NicknameFormat"] = "{roblox_name}"
        await message.channel.send(embed=discord.Embed(
            description = "I've changed the nickname format to {roblox_name} (DEFAULT). Every member who verifies gets their nickname now set by this format.\n\nExample of appearance:\nGodOf_Lua",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
        return

    GuildData["NicknameFormat"] = message.content[0+len(Arguments[0])+1:len(message.content)]
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)

    role = "Owner"
    roblox_name = "GodOf_Lua"
    discord_name = "GodOf_Lua"
    discord_tag = "#2643"

    await message.channel.send(embed=discord.Embed(
        description = "I've changed the nickname format to "+message.content[0+len(Arguments[0])+1:len(message.content)]+". Every member who verifies gets their nickname now set by this format.\n\nExample of appearance:\n"+message.content[0+len(Arguments[0])+1:len(message.content)].format(role=role, roblox_name=roblox_name, discord_name=discord_name, discord_tag=discord_tag),
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))