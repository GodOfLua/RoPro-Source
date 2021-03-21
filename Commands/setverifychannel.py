
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

    if len(Arguments) < 2 and len(message.channel_mentions) < 1:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<ChannelMention | ChannelId | ChannelName or say none>",
            "command": "setverifychannel",
            "length": 1,
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

    if not "VerifyChannel" in GuildData:
        putVerify(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        
    channel = getText(message.content[0+len(Arguments[0])+1:len(message.content)], message.guild.channels, message)

    if channel or message.content[0+len(Arguments[0])+1:len(message.content)].lower() == "none":
        if message.content[0+len(Arguments[0])+1:len(message.content)].lower() == "none":
            GuildData["VerifyChannel"] = "none"
            await message.channel.send(embed=discord.Embed(
                description = "I will  now respond to !verify and !getroles in every channel.",
                footer = "Powered by RoPro Verification System · !invite",
                color = 0x3a9518
            ))
        else:
            GuildData["VerifyChannel"] = str(channel.id) 
            await message.channel.send(embed=discord.Embed(
                description = "I've changed the verify channel to "+channel.mention+". I will only react now to !getroles, !verify in that channel.",
                footer = "Powered by RoPro Verification System · !invite",
                color = 0x3a9518
            ))
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    else:
        await message.channel.send(embed=discord.Embed(
            description = "Make sure to specify an channel\nUsage: !setverifychannel <ChannelMention | ChannelId | ChannelName or say none>",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0xc84c4c
        ))