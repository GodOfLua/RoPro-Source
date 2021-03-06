
import discord 

async def getDM(userObject):
    if userObject.dm_channel:
        return userObject.dm_channel 
    else: 
        await userObject.create_dm()
        return userObject.dm_channel