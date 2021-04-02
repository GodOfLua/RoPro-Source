
# Made by GodOf_Lua

from discord import Embed as Embed
from discord.utils import get
import discord 
from Modules.Discord.Author import  *

async def run(member, Client, Discord_Bot):
    settings = Discord_Bot.catchGuildSettings(member.guild.id)
    if settings["UnverifiedRole"] != 0:
        try:
            role = get(member.guild.roles, id=int(settings["UnverifiedRole"]))
            if role:
                await member.add_roles(role)
        except:
            pass
    dm = await getDM(member)
    await dm.send("Welcome to **"+member.guild.name+"**!")