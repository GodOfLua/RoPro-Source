
import discord
from datetime import datetime

FooterText = "Powered by RoPro System · !invite"

def rolesEmbed(isNickname, addedRolesText, removedRolesText, nicknameText): 
    if isNickname == True:
        embed=discord.Embed(title="RoPro Verification", description=f"Nickname: {nicknameText}", color=0x3a9518, timestamp=datetime.utcnow())
        embed.add_field(name="Added Roles:", value=addedRolesText, inline=True)
        embed.add_field(name="Removed Roles:", value=removedRolesText, inline=True)
        embed.set_footer(text=FooterText)
    elif isinstance(isNickname, str):
        embed=discord.Embed(title="RoPro Verification", description=f"{isNickname}", color=0x3a9518, timestamp=datetime.utcnow())
        embed.add_field(name="Added Roles:", value=addedRolesText, inline=True)
        embed.add_field(name="Removed Roles:", value=removedRolesText, inline=True)
        embed.set_footer(text=FooterText)
    else:
        embed=discord.Embed(title="RoPro Verification", color=0x3a9518, timestamp=datetime.utcnow())
        embed.add_field(name="Added Roles:", value=addedRolesText, inline=True)
        embed.add_field(name="Removed Roles:", value=removedRolesText, inline=True)
        embed.set_footer(text=FooterText)
    return embed

def missingBinds():
    embed=discord.Embed(title="Missing records", description="There are currently no bound roblox group to this guild, run !bindgroup to bind one.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def missingAccBinds():
    embed=discord.Embed(title="Missing records", description="There are currently no bound roblox accounts to this user, run !bindaccount or !verify to bind one.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def working():
    embed=discord.Embed(description="Working..", color=0xba981c)
    embed.set_footer(text=FooterText)
    return embed

def bindAccountUser():
    embed=discord.Embed(title="Bind an account", description="Please respond with your username in order to countine with the process of binding an account. Prompt will expire in 60 seconds.", color=0xc337ac)
    embed.set_footer(text=FooterText)
    return embed

def bindAccountDone():
    embed=discord.Embed(title="Bind an account", description="Join this game\nhttps://www.roblox.com/games/6454158111/Verify-Center to verify that you own this roblox account.", color=0xc337ac)
    return embed

def bindAccountDone2():
    embed=discord.Embed(description="Once you joined the game reply to this dm with `done` or let the prompt expire. Prompt expires in 300 seconds.", color=0xc337ac)
    embed.set_footer(text=FooterText)
    return embed

def apiError():
    embed=discord.Embed(description="API error, try again later.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def timeout():
    embed=discord.Embed(description="Prompt has expired.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def cancel():
    embed=discord.Embed(description="Prompt has been cancelled.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def invalidUser():
    embed=discord.Embed(description="Invalid username.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def invalidStatus():
    embed=discord.Embed(description="I were unable to find the code in your about/feed make sure you putted it without any other words in your about/feed\nRetry the process with the bindaccount command.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def valStatus():
    embed=discord.Embed(description="Successfully bound your roblox account. You can now use verify, getroles and update to receive your roles.", color=0x3a9518)
    embed.set_footer(text=FooterText)
    return embed

def unbound():
    embed=discord.Embed(description="Your roblox account has been unbound.", color=0x3a9518)
    embed.set_footer(text=FooterText)
    return embed

def alreadyExistUser():
    embed=discord.Embed(description="This roblox user already exists in bindings. If you wish to bind an different account call bindaccount again.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def argument(data):
    embed=discord.Embed(description="The command "+data["command"]+" requires "+str(data["length"])+" "+str(data["pronounce"])+"\nUsage: !"+str(data["command"])+" "+data["arguments"], color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def numeric(data):
    embed=discord.Embed(description="The argument "+data["nameofError"]+" requires a number." , color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def notFound():
    embed=discord.Embed(description="I was unable to find the mentioned account in your bindings.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def role():
    embed=discord.Embed(description="I was unable to find a role, make sure to mention a role or give me a id or the name.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def rankRangeError():
    embed=discord.Embed(description="Make sure to give me an valid RankRange to see what an rankrange is call !help verification.", color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def permissionError(data):
    embed=discord.Embed(description="User is missing the following permissions: "+data["permission"], color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def bindingEmbed(data):
    embed=discord.Embed(title="Guild bindings", description=data, color=0xc337ac)
    embed.set_footer(text=FooterText)
    return embed

def bindingEmbed1(data):
    embed=discord.Embed(title="Rank bindings", description=data, color=0xc337ac)
    embed.set_footer(text=FooterText)
    return embed

def bindError():
    embed=discord.Embed(description="Group not found in database."+data["permission"], color=0xc84c4c)
    embed.set_footer(text=FooterText)
    return embed

def dms():
    embed=discord.Embed(description="Check your dms! (Make sure your dms are open.)",color=0xc337ac)
    embed.set_footer(text=FooterText)
    return embed

async def throw(code, Method):
    if code == "noBoundGroups":
        await Method(embed=missingBinds())
    elif code == "noBoundAccounts":
        await Method(embed=missingAccBinds())
    elif code == "workingMethod":
        return await Method(embed=working())
    elif code == "apiError":
        await Method(embed=apiError())
    elif code == "checkDM":
        await Method(embed=dms())
    elif code == "timeout":
        await Method(embed=timeout())
    elif code == "cancel":
        await Method(embed=cancel())
    elif code == "invalidUser":
        await Method(embed=invalidUser())
    elif code == "invalidStatus":
        await Method(embed=invalidStatus())
    elif code == "valStatus":
        await Method(embed=valStatus())
    elif code == "userExist":
        await Method(embed=alreadyExistUser())
    elif code == "argumentError":
        await Method["method"](embed=argument(Method))
    elif code == "numericError":
        await Method["method"](embed=numeric(Method))
    elif code == "unbound":
        await Method(embed=unbound())
    elif code == "notFound":
        await Method(embed=notFound())
    elif code == "roleError":
        await Method(embed=role())
    elif code == "rankRangeError":
        await Method(embed=rankRangeError())
    elif code == "permissionError":
        await Method["method"](embed=permissionError(Method))
    elif code == "bindError":
        await Method(embed=bindError)
    