
import json 
import asyncio 
import discord 
from discord.utils import get

async def run(message, Arguments, Client, Discord_Bot):
    settings = Discord_Bot.catchGuildSettings(str(message.guild.id))
    count = 0
    verificationChannel = "None"
    primary = "None"

    if settings["VerifyChannel"] != "none":
        if get(message.guild.channels, id=int(settings["VerifyChannel"])):
            verificationChannel = get(message.guild.channels, id=int(settings["VerifyChannel"])).mention

    if settings["PrimaryNickname"] != "none":
        primary = settings["PrimaryNickname"]

    for i in settings["BOUND_GROUPS"]:
        i = settings["BOUND_GROUPS"][i]
        count += len(i["BINDING"])

    embed=discord.Embed(title="Settings", description="Current guild settings", color=0xc337ac)
    embed.add_field(name="Prefix", value=settings["SERVER_PREFIX"], inline=False)
    embed.add_field(name="Total bindings", value=str(count), inline=False)
    embed.add_field(name="Total acronyms", value=str(len(settings["Acronyms"])), inline=False)
    embed.add_field(name="Verification channel", value=verificationChannel, inline=False)
    embed.add_field(name="Primary group", value=primary, inline=False)
    embed.add_field(name="Nickames", value="Enabled", inline=False)

    await message.channel.send(embed=embed)