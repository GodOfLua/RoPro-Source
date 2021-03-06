
# Made by GodOf_Lua

from Modules.DataManagement import *
from Modules.Discord.Embeds import *
from Modules.Discord.Author import *
from Modules.Discord.Prompts import *
from Modules.Discord.RankRange import *
from Modules.Discord.Roles import *
from Modules.RandomGenerators.generateCode import *
from discord.utils import get
import discord
import json
import requests

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


async def setcookie(message, Arguments, Client):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId]",
            "command": "setcookie",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    GroupId = Arguments[1]

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.administrator

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`ADMINISTRATOR`"
        })
        return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    SpecifiedGuildData = GuildData

    await throw("checkDM", ReplyMethod)

    dm = await getDM(Author)

    msg = await executePromptDM(Client, dm.send, discord.Embed(
        title = "Set the bot cookie of your roblox group", 
        description = "Please respond with the .ROBLOSECURITY cookie of your bot account. (Make sure to make an seperate one) The cookie is required to login into the account and perform rank changes so commands such as promote are able to work. If you don't know how to get the cookie please click [here](https://www.youtube.com/watch?v=KIMT82TLS9I)\nThe prompt will expire in 300 seconds.",
        color = 0xc337ac,
    ), message, 300)

    if msg == "cancel" or msg == "timeout":
        await throw(msg, dm)
        return 

    if not GroupId in SpecifiedGuildData["BOUND_GROUPS"]:
        SpecifiedGuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", SpecifiedGuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData = GuildData


    SpecifiedGuildData["BOUND_GROUPS"][GroupId]["COOKIE"] = msg.content
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", SpecifiedGuildData)
    await dm.send(embed=discord.Embed(
        description = "Cookie of your group has been successfully added/updated",
        color = 0x3a9518
    ))

def groupexist(serverid,groupid):
    network = requests.get("https://groups.roblox.com/v1/groups/"+groupid)
    if network.status_code == 200:
        return json.loads(network.text)
    else:
        return "unavailable"

async def promote(message, Arguments):

    if len(Arguments) < 3 or (len(Arguments) < 2 and len(message.mentions) < 1):
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId] [Username]",
            "command": "promote",
            "length": 2,
            "pronounce": "Arguments"
        })
        return

    GroupId = Arguments[1]

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })
        return

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.manage_roles

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`MANAGE_ROLES`"
        })
        return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not GroupId in GuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    mainMSG = await throw("workingMethod", ReplyMethod)
    user = Arguments[2]
    embed = discord.Embed()
    embed.set_footer(text="Powered by RoPro Verification System · !invite")

    try:
        message.mentions[0]
        id = message.mentions[0].id
        d = getData(f"./Data/User_Data/{id}.json")
        if d:
            if len(d["BoundAccounts"]) > 0:
                user = d["BoundAccounts"][d["SelectedAccountIndex"]]["Username"]
    except:
        pass

    # Check if user exists

    userResponse = requests.get("http://api.roblox.com/users/get-by-username?username="+user)

    if userResponse.status_code == 200:
        userResponse = json.loads(userResponse.text)
        if not "Id" in userResponse:
            embed.description = "User dosen't exist."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Check if group exists

    groupExist = groupexist(0, GroupId)

    if groupExist == "unavailable":
        embed.description = "API error or invalid group Id."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Check if user is in group 

    groupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(userResponse["Id"])+"/groups/roles?limit=100")

    if groupResponse.status_code == 200:
        Found = False
        UserIndex = 0
        groupResponse = json.loads(groupResponse.text)
        for i in groupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            UserIndex += 1

        if Found == False:
            embed.description = "User not in group."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Verify Cookie
    
    verCookie = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])

    if verCookie != 200:
        embed.description = "API error or invalid cookie."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Check bot

    cookie = GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        getBotUserSession = requests.get("https://www.roblox.com/my/profile", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        if getBotUserSession.status_code == 200:
            getBotUserSession = json.loads(getBotUserSession.text)
        else:
            await mainMSG.edit(embed=apiError())
            return
    else:
        embed.description = "Unable to get X-CSRF-TOKEN"
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return 

    botId = getBotUserSession["UserId"]
    botGroupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(botId)+"/groups/roles?limit=100")

    if botGroupResponse.status_code == 200:
        Found = False
        Index = 0
        botGroupResponse = json.loads(botGroupResponse.text)
        for i in botGroupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            Index +=1

        if Found == False:
            embed.description = "Bot not in group."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return 
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Check bot rank

    if groupResponse["data"][UserIndex]["role"]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
        embed.description = "User role to promote to is higher than or same with bot role."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Get Group Role

    rolesResponse = requests.get("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/roles", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rolesResponse.status_code == 200:
        rolesResponse = json.loads(rolesResponse.text)
        RoleIndex = 0
        for i in rolesResponse["roles"]:
            if i["id"] == groupResponse["data"][UserIndex]["role"]["id"]:
                break
            RoleIndex += 1

        try:
            rolesResponse["roles"][RoleIndex+1]
        except:
            embed.description = "User has already highest role."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return 

        if rolesResponse["roles"][RoleIndex+1]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
            embed.description = "Role to promote to is higher than or same with bot role."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return           
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Rank User

    rankRequest = requests.patch("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/users/"+str(userResponse["Id"]), data=json.dumps({
        "roleId": rolesResponse["roles"][RoleIndex+1]["id"]
    }), headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rankRequest.status_code == 200:
        embed.description = userResponse["Username"]+" has been promoted to "+rolesResponse["roles"][RoleIndex+1]["name"]
        embed.color = 0x3a9518
        await mainMSG.edit(embed=embed)
    else:
        embed.description = "Unable to promote user."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    return True

async def demote(message, Arguments):

    if len(Arguments) < 3 or (len(Arguments) < 2 and len(message.mentions) < 1):
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId] [Username]",
            "command": "demote",
            "length": 2,
            "pronounce": "Arguments"
        })
        return

    GroupId = Arguments[1]

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })
        return

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.manage_roles

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`MANAGE_ROLES`"
        })
        return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not GroupId in GuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    mainMSG = await throw("workingMethod", ReplyMethod)
    user = Arguments[2]
    embed = discord.Embed()
    embed.set_footer(text="Powered by RoPro Verification System · !invite")

    try:
        message.mentions[0]
        id = message.mentions[0].id
        d = getData(f"./Data/User_Data/{id}.json")
        if d:
            if len(d["BoundAccounts"]) > 0:
                user = d["BoundAccounts"][d["SelectedAccountIndex"]]["Username"]
    except:
        pass

    # Check if user exists

    userResponse = requests.get("http://api.roblox.com/users/get-by-username?username="+user)

    if userResponse.status_code == 200:
        userResponse = json.loads(userResponse.text)
        if not "Id" in userResponse:
            embed.description = "User dosen't exist."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Check if group exists

    groupExist = groupexist(0, GroupId)

    if groupExist == "unavailable":
        embed.description = "API error or invalid group Id."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Check if user is in group 

    groupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(userResponse["Id"])+"/groups/roles?limit=100")

    if groupResponse.status_code == 200:
        Found = False
        UserIndex = 0
        groupResponse = json.loads(groupResponse.text)
        for i in groupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            UserIndex += 1

        if Found == False:
            embed.description = "User not in group."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Verify Cookie
    
    verCookie = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])

    if verCookie != 200:
        embed.description = "API error or invalid cookie."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Check bot

    cookie = GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        getBotUserSession = requests.get("https://www.roblox.com/my/profile", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        if getBotUserSession.status_code == 200:
            getBotUserSession = json.loads(getBotUserSession.text)
        else:
            await mainMSG.edit(embed=apiError())
            return
    else:
        embed.description = "Unable to get X-CSRF-TOKEN"
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return 

    botId = getBotUserSession["UserId"]
    botGroupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(botId)+"/groups/roles?limit=100")

    if botGroupResponse.status_code == 200:
        Found = False
        Index = 0
        botGroupResponse = json.loads(botGroupResponse.text)
        for i in botGroupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            Index +=1

        if Found == False:
            embed.description = "Bot not in group."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return 
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Check bot rank

    if groupResponse["data"][UserIndex]["role"]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
        embed.description = "User role to demote to is higher than or same with bot role."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Get Group Role

    rolesResponse = requests.get("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/roles", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rolesResponse.status_code == 200:
        rolesResponse = json.loads(rolesResponse.text)
        RoleIndex = 0
        for i in rolesResponse["roles"]:
            if i["id"] == groupResponse["data"][UserIndex]["role"]["id"]:
                break
            RoleIndex += 1

        try:
            rolesResponse["roles"][RoleIndex-1]
        except:
            embed.description = "I were unable to find the next lower role."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return 

        if rolesResponse["roles"][RoleIndex-1]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
            embed.description = "Role to demote to is higher than or same with bot role."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return           
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Rank User

    rankRequest = requests.patch("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/users/"+str(userResponse["Id"]), data=json.dumps({
        "roleId": rolesResponse["roles"][RoleIndex-1]["id"]
    }), headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rankRequest.status_code == 200:
        embed.description = userResponse["Username"]+" has been demoted to "+rolesResponse["roles"][RoleIndex-1]["name"]
        embed.color = 0x3a9518
        await mainMSG.edit(embed=embed)
    else:
        embed.description = "Unable to demote user."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    return True

async def setrank(message, Arguments):

    if len(Arguments) < 4 or (len(Arguments) < 3 and len(message.mentions) < 1):
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId] [Username] [Rank]",
            "command": "setrank",
            "length": 3,
            "pronounce": "Arguments"
        })
        return

    GroupId = Arguments[1]
    Rank = Arguments[3]

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })
        return

    if not Rank.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "Rank"
        })
        return

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.manage_roles

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`MANAGE_ROLES`"
        })
        return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not GroupId in GuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    mainMSG = await throw("workingMethod", ReplyMethod)
    user = Arguments[2]
    embed = discord.Embed()
    embed.set_footer(text="Powered by RoPro Verification System · !invite")

    try:
        message.mentions[0]
        id = message.mentions[0].id
        d = getData(f"./Data/User_Data/{id}.json")
        if d:
            if len(d["BoundAccounts"]) > 0:
                user = d["BoundAccounts"][d["SelectedAccountIndex"]]["Username"]
    except:
        pass

    # Check if user exists

    userResponse = requests.get("http://api.roblox.com/users/get-by-username?username="+user)

    if userResponse.status_code == 200:
        userResponse = json.loads(userResponse.text)
        if not "Id" in userResponse:
            embed.description = "User dosen't exist."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Check if group exists

    groupExist = groupexist(0, GroupId)

    if groupExist == "unavailable":
        embed.description = "API error or invalid group Id."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Check if user is in group 

    groupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(userResponse["Id"])+"/groups/roles?limit=100")

    if groupResponse.status_code == 200:
        Found = False
        UserIndex = 0
        groupResponse = json.loads(groupResponse.text)
        for i in groupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            UserIndex += 1

        if Found == False:
            embed.description = "User not in group."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Verify Cookie
    
    verCookie = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])

    if verCookie != 200:
        embed.description = "API error or invalid cookie."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Check bot

    cookie = GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        getBotUserSession = requests.get("https://www.roblox.com/my/profile", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        if getBotUserSession.status_code == 200:
            getBotUserSession = json.loads(getBotUserSession.text)
        else:
            await mainMSG.edit(embed=apiError())
            return
    else:
        embed.description = "Unable to get X-CSRF-TOKEN"
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return 

    botId = getBotUserSession["UserId"]
    botGroupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(botId)+"/groups/roles?limit=100")

    if botGroupResponse.status_code == 200:
        Found = False
        Index = 0
        botGroupResponse = json.loads(botGroupResponse.text)
        for i in botGroupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            Index +=1

        if Found == False:
            embed.description = "Bot not in group."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return 
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Check bot rank

    if groupResponse["data"][UserIndex]["role"]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
        embed.description = "User role is higher than or same with bot role."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    # Get Group Role

    rolesResponse = requests.get("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/roles", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rolesResponse.status_code == 200:
        rolesResponse = json.loads(rolesResponse.text)
        RoleIndex = 0
        for i in rolesResponse["roles"]:
            if i["id"] == groupResponse["data"][UserIndex]["role"]["id"]:
                break
            RoleIndex += 1

        roleDesg = 0
        for i in rolesResponse["roles"]:
            if i["rank"] == int(Rank):
                break
            roleDesg += 1

        try:
            rolesResponse["roles"][roleDesg]
        except:
            embed.description = "I were unable to find the role with the specifiedd rank."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return 

        if rolesResponse["roles"][roleDesg]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
            embed.description = "Role to set rank to is higher than or same with bot role."
            embed.color = 0xc84c4c
            await mainMSG.edit(embed=embed)
            return           
    else:
        await mainMSG.edit(embed=apiError())
        return

    # Rank User

    rankRequest = requests.patch("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/users/"+str(userResponse["Id"]), data=json.dumps({
        "roleId": rolesResponse["roles"][roleDesg]["id"]
    }), headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rankRequest.status_code == 200:
        embed.description = userResponse["Username"]+" role has been changed to "+rolesResponse["roles"][roleDesg]["name"]
        embed.color = 0x3a9518
        await mainMSG.edit(embed=embed)
    else:
        embed.description = "Unable to set the rank of the user to the specified one."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    return True 

def valCookie(cookie):
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        network = requests.get("https://api.roblox.com/currency/balance", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        return network.status_code
    else:
        return "Unable to fetch X_CSRF_TOKEN"

async def checkCookie(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId]",
            "command": "valcookie",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    GroupId = Arguments[1]

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.administrator

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`ADMINISTRATOR`"
        })
        return

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not GuildData:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    mainMsg = await throw("workingMethod", message.channel.send)

    if not GroupId in GuildData["BOUND_GROUPS"]:
        await mainMsg.edit(embed=discord.Embed(
            title = "Missing records",
            description = "This group wasn't bound yet or has set a cookie. Call !setcookie or !bind to fix that.",
            color = 0xc84c4c
        ))
        return
    
    if not "COOKIE" in GuildData["BOUND_GROUPS"][GroupId]:
        await mainMsg.edit(embed=discord.Embed(
            title = "Missing records",
            description = "There was no cookie set yet to this group. Call !setcookie to fix that.",
            color = 0xc84c4c
        ))
        return

    ret = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])
    if ret == 200:
        await mainMsg.edit(embed=discord.Embed(
            title = "Valid cookie",
            description = "This cookie is valid.",
            color = 0x3a9518
        ))
    else:
        await mainMsg.edit(embed=discord.Embed(
            title = "Invalid cookie or api error.",
            description = "This cookie is invalid or an API error occoured.",
            color = 0xc84c4c
        ))