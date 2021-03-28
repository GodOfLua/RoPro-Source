
# Made by GodOf_Lua

from discord import Embed as Embed
from discord.utils import get

async def run(member, Client, Discord_Bot):
    settings = Client.catchGuildSettings(member.Guild.id)
    if settings["UnverifiedRole"] == 0:
        Role = get(message.guild.roles, name="Unverified")
        Role2 = get(message.guild.roles, name="unverified")
        if not Role and Role2:
            Role2 = Role
        if not Role and not Role2:
            Role = await message.guild.create_role(name="Unverified", hoist=False)
        GuildData["UnverifiedRole"] = Role.id
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)