import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
from Modules.Discord.Author import *
import secrets
import time

async def run(message, Arguments, Client, Discord_Bot):
    before = time.monotonic()
    message = await message.channel.send(embed=discord.Embed(
        description = "Measuring..",
        color = 0x3a9518
    ))
    ping = round((time.monotonic() - before) * 1000,2)
    await message.edit(embed=discord.Embed(
        description = "Pong!\nPing: "+str(ping)+"ms\nBot latency: "+str(round(int(Client.latency),2))+"ms",
        color = 0x3a9518
    ))