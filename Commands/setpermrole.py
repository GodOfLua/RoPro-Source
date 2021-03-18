
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
    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<RoleMention | RoleId | RoleName>",
            "command": "setpermrole",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    Admin = Author.guild_permissions.administrator

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`ADMINISTRATOR`"
        })
        return

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Arguments[1].lower() == "none":
        GuildData["modrole"] = 0
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        await message.channel.send(embed=discord.Embed(
            description = "Bot permissions from role has been removed.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
        return

    role = getRole(message.content[0+len(Arguments[0])+1:len(message.content)], message.guild.roles, message)
    if not role:
        await throw("roleError", ReplyMethod)
        return

    GuildData["modrole"] = role.id
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    await message.channel.send(embed=discord.Embed(
        description = role.mention+" has been set as the permissions role.",
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))