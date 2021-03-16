
import asyncio 
import discord

async def executePromptDM(Client, sendMethod,  embed, message, timeout):
    await sendMethod(embed=embed)
    try:
        msg = await Client.wait_for('message', check=lambda m: m.author == message.author and m.channel.type == discord.ChannelType.private, timeout=timeout)
        if msg.content.lower() == "cancel":
            return "cancel"
        return msg
    except asyncio.TimeoutError:
        return "timeout"

async def executePrompt(Client, sendMethod,  embed, message, timeout, word):
    await sendMethod(embed=embed)
    try:
        msg = await Client.wait_for('message', check=lambda m: m.author == message.author and m.channel.type == discord.ChannelType.text and m.content.lower() == word, timeout=timeout)
        if msg.content.lower() == "cancel":
            return "cancel"
        return msg
    except asyncio.TimeoutError:
        return "timeout"