
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

async def acronyms(message, Arguments, Client, Discord_Bot):

    Author = message.author
    Guild = message.guild
    GuildId = str(message.guild.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "Acronyms" in GuildData:
        putAcronyms(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    Text = ""

    if len(GuildData["Acronyms"]) < 1:
        await message.channel.send(embed=discord.Embed(
            description = "This guild dosen't have any acronyms.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))  
        return

    for i in GuildData["Acronyms"]:
        Text = Text+"\n\nOrginal name: "+i+"\nShort name: "+GuildData["Acronyms"][i]

    await message.channel.send(embed=discord.Embed(
        description = Text,
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))  