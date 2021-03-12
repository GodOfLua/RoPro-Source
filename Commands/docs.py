
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
from Modules.Discord.Author import *
import secrets

async def run(message, Arguments, Client, Discord_Bot):
    await dm.send(embed=discord.Embed(
        description = "[Click here!](https://ropro.xyz/docs/)",
        color = 0x3a9518
    ))