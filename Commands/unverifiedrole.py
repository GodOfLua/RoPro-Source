
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
from Modules.Discord.Roles import *

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
    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    try:
        Arguments[1]
    except:
        Role = get(message.guild.roles, name="Unverified")
        Role2 = get(message.guild.roles, name="unverified")
        if not Role and Role2:
            Role2 = Role
        if not Role and not Role2:
            Role = await message.guild.create_role(name="Unverified", hoist=False)
        GuildData["UnverifiedRole"] = Role.id
        await message.channel.send(embed=discord.Embed(
            description = Role.mention + " has been created/set as unverified role.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        return

    if Arguments[1].lower() == "none":
        GuildData["UnverifiedRole"] = 0
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        await message.channel.send(embed=discord.Embed(
            description = "Unverified role has been removed.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
        return

    role = getRole(message.content[0+len(Arguments[0])+1:len(message.content)], message.guild.roles, message)
    if not role:
        await throw("roleError", ReplyMethod)
        return

    GuildData["UnverifiedRole"] = role.id
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    await message.channel.send(embed=discord.Embed(
        description = role.mention+" has been set as the unverified role.",
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))