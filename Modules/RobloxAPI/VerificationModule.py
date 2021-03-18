
# Made by GodOf_Lua

# Get All Modules
# pylint: disable=no-member

from Modules.DataManagement import *
from Modules.Discord.Embeds import *
from Modules.Discord.Author import *
from Modules.Discord.Prompts import *
from Modules.Discord.RankRange import *
from Modules.Discord.Roles import *
from Modules.Discord.Channel import *
from Modules.RandomGenerators.generateCode import *
from discord.utils import get
import discord
import requests

async def acronyms(message, Arguments):

    Author = message.author
    Guild = message.guild
    GuildId = str(message.guild.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "Acronyms" in GuildData:
        putAcronyms(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    Text = ""

    if len(GuildData["Acronyms"]) < 1:
        await message.channel.send(embed=discord.Embed(
            description = "This guild dosen't have any acronyms.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))  
        return

    for i in GuildData["Acronyms"]:
        Text = Text+"\n\nOrginal name: "+i+"\nShort name: "+GuildData["Acronyms"][i]

    await message.channel.send(embed=discord.Embed(
        description = Text,
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))  

async def addAcronym(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<StringFormat2 (Example: Level - 1:L1)>",
            "command": "addacronym",
            "length": 1,
            "pronounce": "Argument"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "Acronyms" in GuildData:
        putAcronyms(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    x = message.content[0+len(Arguments[0])+1:len(message.content)].split(":")

    if len(x) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<StringFormat2 (Example: Level - 1:L1)>",
            "command": "addacronym",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    GuildData["Acronyms"][x[0]] = x[1]

    await message.channel.send(embed=discord.Embed(
        description = x[0]+" will now be displayed in nicknames as "+x[1],
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))

    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)

async def delAcronym(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<String>",
            "command": "delacronym",
            "length": 1,
            "pronounce": "Argument"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "Acronyms" in GuildData:
        putAcronyms(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    x = message.content[0+len(Arguments[0])+1:len(message.content)]

    try:
        del GuildData["Acronyms"][x]
    except:
        await message.channel.send(embed=discord.Embed(
            description = "I was unable to find the specified acronym.",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
        return

    await message.channel.send(embed=discord.Embed(
        description = "I removed your specified acronym.",
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))

    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)

async def setNickname(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<StringFormat (Example: {rank} | {roname}, for more magic words view !magicwords)>",
            "command": "setnickname",
            "length": 1,
            "pronounce": "Argument"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "NicknameFormat" in GuildData:
        putnickformat(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if len(message.content[0+len(Arguments[0])+1:len(message.content)]) < 1:
        GuildData["NicknameFormat"] = "{roblox_name}"
        await message.channel.send(embed=discord.Embed(
            description = "I've changed the nickname format to {roblox_name} (DEFAULT). Every member who verifies gets their nickname now set by this format.\n\nExample of appearance:\nGodOf_Lua",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
        return

    GuildData["NicknameFormat"] = message.content[0+len(Arguments[0])+1:len(message.content)]
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)

    role = "Owner"
    roblox_name = "GodOf_Lua"
    discord_name = "GodOf_Lua"
    discord_tag = "#2643"

    await message.channel.send(embed=discord.Embed(
        description = "I've changed the nickname format to "+message.content[0+len(Arguments[0])+1:len(message.content)]+". Every member who verifies gets their nickname now set by this format.\n\nExample of appearance:\n"+message.content[0+len(Arguments[0])+1:len(message.content)].format(role=role, roblox_name=roblox_name, discord_name=discord_name, discord_tag=discord_tag),
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))

async def setprimary(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<GroupId or say none>",
            "command": "setprimary",
            "length": 1,
            "pronounce": "Argument"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "PrimaryNickname" in GuildData:
        putprimary(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not Arguments[1].isnumeric() and Arguments[1] != "none":
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

    GuildData["PrimaryNickname"] = Arguments[1]
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)

    if Arguments[1] == "none":
        await message.channel.send(embed=discord.Embed(
            description = "I will now prioritize all groups equal. (This is only important if your using the magic word {role})",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))
    else:
        await message.channel.send(embed=discord.Embed(
            description = "I will now prioritize this group in the nickname format. (This is only important if your using the magic word {role})",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0x3a9518
        ))

async def setVerifyChannel(message, Arguments):

    if len(Arguments) < 2 and len(message.channel_mentions) < 1:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "<ChannelMention | ChannelId | ChannelName or say none>",
            "command": "setverifychannel",
            "length": 1,
            "pronounce": "Arguments"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "VerifyChannel" in GuildData:
        putVerify(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        
    channel = getText(message.content[0+len(Arguments[0])+1:len(message.content)], message.guild.channels, message)

    if channel or message.content[0+len(Arguments[0])+1:len(message.content)].lower() == "none":
        if message.content[0+len(Arguments[0])+1:len(message.content)].lower() == "none":
            GuildData["VerifyChannel"] = "none"
            await message.channel.send(embed=discord.Embed(
                description = "I will  now respond to !verify and !getroles in every channel.",
                footer = "Powered by RoPro Verification System · !invite",
                color = 0x3a9518
            ))
        else:
            GuildData["VerifyChannel"] = str(channel.id) 
            await message.channel.send(embed=discord.Embed(
                description = "I've changed the verify channel to "+channel.mention+". I will only react now to !getroles, !verify in that channel.",
                footer = "Powered by RoPro Verification System · !invite",
                color = 0x3a9518
            ))
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    else:
        await message.channel.send(embed=discord.Embed(
            description = "Make sure to specify an channel\nUsage: !setverifychannel <ChannelMention | ChannelId | ChannelName or say none>",
            footer = "Powered by RoPro Verification System · !invite",
            color = 0xc84c4c
        ))
        

async def listBindings(message, Arguments):

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if len(Arguments) > 1:
        if Arguments[1] in GuildData["BOUND_GROUPS"]:
            textGen = ""
            embed=discord.Embed(title="Guild bindings", color=0xc337ac)
            embed.set_footer(text=FooterText)
            for i in GuildData["BOUND_GROUPS"][Arguments[1]]["BINDING"]:
                if get(message.guild.roles, id=i["roleId"]):
                    embed.add_field(name="Role: "+get(message.guild.roles, id=i["roleId"]).mention+" ( "+get(message.guild.roles, id=i["roleId"]).name+" )",inline=False,value="Minimum rank: "+str(i["min"])+"\nMaximum rank: "+str(i["max"]))
            await ReplyMethod(embed=embed)
        else:
            return
    else:
        textGen = ""
        for i in GuildData["BOUND_GROUPS"]:
            i = GuildData["BOUND_GROUPS"][str(i)]
            data = requests.get("https://groups.roblox.com/v1/groups/"+str(i["ID"]))
            if data.status_code == 200 and len(i["BINDING"]) > 0:
                textGen = textGen+"\n\n"+json.loads(data.text)["name"]+"\nrun !bindings "+str(i["ID"])+" to see rank bindings."
        await ReplyMethod(embed=bindingEmbed(textGen))


async def bind(message, Arguments):

    if len(Arguments) < 4:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId] [RankRange] [RoleMention | RoleId | RoleName]",
            "command": "bind",
            "length": 3,
            "pronounce": "Arguments"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    SpecifiedGuildData = GuildData

    GroupId = Arguments[1]
    RankRange = getRankRange(Arguments[2])
    Role = getRole(message.content[0+len(Arguments[0])+2+len(Arguments[1])+1+len(Arguments[2]):len(message.content)], message.guild.roles, message)

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })
        return

    if not Role:
        await throw("roleError", ReplyMethod)
        return

    if not RankRange:
        await throw("rankRangeError", ReplyMethod)
        return

    if not GroupId in SpecifiedGuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData = GuildData

    SpecifiedGuildData["BOUND_GROUPS"][GroupId]["BINDING"].append({
        "roleId": Role.id,
        "min": RankRange["min"],
        "max": RankRange["max"]
    })
    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    GuildData = SpecifiedGuildData
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    await message.channel.send(embed=discord.Embed(
        description = "Bind has been added.",
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))

async def unbind(message, Arguments):

    if len(Arguments) < 3:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId] [RoleMention | RoleId | RoleName]",
            "command": "unbind",
            "length": 2,
            "pronounce": "Arguments"
        })
        return

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

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    SpecifiedGuildData = GuildData

    GroupId = Arguments[1]
    Role = getRole(message.content[0+len(Arguments[0])+2+len(Arguments[1]):len(message.content)], message.guild.roles, message)

    if not GroupId.isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

    if not Role:
        await throw("roleError", ReplyMethod)

    if not GroupId in SpecifiedGuildData["BOUND_GROUPS"]:
        await throw("bindError", ReplyMethod)

    Removed = 0
    Index = 0
    for i in SpecifiedGuildData["BOUND_GROUPS"][GroupId]["BINDING"]:
        if str(i["roleId"]) == str(Role.id):
            Removed += 1
            SpecifiedGuildData["BOUND_GROUPS"][GroupId]["BINDING"].pop(Index)

        Index += 1
    
    if len(SpecifiedGuildData["BOUND_GROUPS"][GroupId]["BINDING"]) < 1:
        del SpecifiedGuildData["BOUND_GROUPS"][GroupId]

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    GuildData = SpecifiedGuildData
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
    await message.channel.send(embed=discord.Embed(
        description = str(Removed) + " bind(s) have been removed associated with this role.",
        footer = "Powered by RoPro Verification System · !invite",
        color = 0x3a9518
    ))

async def Verification(message, auth, Command):
    
    Author = message.author
    Guild = message.guild

    if auth:
        Author = auth

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    ReplyMethod = message.channel.send

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if UserData == None:
        createAuthorData(AuthorId)
        UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    if not "VerifyChannel" in GuildData:
        putVerify(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if GuildData["VerifyChannel"] != "none" and (Command == "verify" or Command == "getroles"):
        if str(message.channel.id) != GuildData["VerifyChannel"]:
            return

    SpecifiedGuildData = GuildData
    SpecifiedUserData = UserData
    
    if len(SpecifiedGuildData["BOUND_GROUPS"]) < 1:
        await throw("noBoundGroups", ReplyMethod)
        return

    if len(SpecifiedUserData["BoundAccounts"]) < 1:
        await throw("noBoundAccounts", ReplyMethod)
        return

    mainMessage = await throw("workingMethod", ReplyMethod)
    
    try:
        boundAccount = SpecifiedUserData["BoundAccounts"][SpecifiedUserData["SelectedAccountIndex"]]
    except:
        try:
            boundAccount = SpecifiedUserData["BoundAccounts"][SpecifiedUserData["SelectedAccountIndex"][0]]
        except:
            pass 
        pass

    if not "RoNick" in GuildData:
        putRoNick(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        SpecifiedGuildData = GuildData
    
    if not "NicknameFormat" in GuildData:
        putnickformat(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not "PrimaryNickname" in GuildData:
        putprimary(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    AddedRoles = ""
    RemovedRoles = ""
    
    userGroups = requests.get("https://groups.roblox.com/v1/users/"+str(boundAccount["Id"])+"/groups/roles?limit=100")

    if userGroups.status_code != 200:
        try:
            await mainMessage.delete()
        except:
            pass
        await throw("apiError", ReplyMethod)
        return

    try:
        userGroups = json.loads(userGroups.text)
    except:
        try:
            await mainMessage.delete()
        except:
            pass
        await throw("apiError", ReplyMethod)
        return

    groupTable = {}

    for i in userGroups["data"]:
        groupTable[str(i["group"]["id"])] = {
            "id": str(i["group"]["id"]),
            "role": i["role"]
        }

    if not "Acronyms" in GuildData:
        putAcronyms(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    Nickname = False
    if SpecifiedGuildData["RoNick"]:
        try:
            discord_tag = "#"+str(Author.discriminator)
            discord_name = Author.name
            roblox_name = boundAccount["Username"]
            role = ""

            for bind in SpecifiedGuildData["BOUND_GROUPS"]:
                bind = SpecifiedGuildData["BOUND_GROUPS"][bind]
                for i in bind["BINDING"]:
                    if bind["ID"] in groupTable:
                        role = groupTable[bind["ID"]]["role"]["name"]
                        if GuildData["PrimaryNickname"] == bind["ID"]:
                            break

            if role in GuildData["Acronyms"]:
                role = GuildData["Acronyms"][role]

            Format = GuildData["NicknameFormat"].format(role=role, roblox_name=roblox_name, discord_name=discord_name, discord_tag=discord_tag)

            await Author.edit(nick=Format)
            Nickname = True 
        except:
            discord_tag = Author.discriminator
            discord_name = Author.name
            roblox_name = boundAccount["Username"]
            role = ""

            for bind in SpecifiedGuildData["BOUND_GROUPS"]:
                bind = SpecifiedGuildData["BOUND_GROUPS"][bind]
                for i in bind["BINDING"]:
                    if bind["ID"] in groupTable:
                        role = groupTable[bind["ID"]]["role"]["name"]
                        if GuildData["PrimaryNickname"] == bind["ID"]:
                            break

            if role in GuildData["Acronyms"]:
                role = GuildData["Acronyms"][role]

            Format = GuildData["NicknameFormat"].format(role=role, roblox_name=roblox_name, discord_name=discord_name, discord_tag=discord_tag)
            Nickname = "I couldn't update your nickname as it seems your role is higher than mine. Your nickname is supposed to be:\n"+Format

    AddedList = []
    for bind in SpecifiedGuildData["BOUND_GROUPS"]:
        bind = SpecifiedGuildData["BOUND_GROUPS"][bind]
        for i in bind["BINDING"]:
            if bind["ID"] in groupTable:
                role = groupTable[bind["ID"]]["role"]
                if int(role["rank"]) >= int(i["min"]) and int(role["rank"]) <= int(i["max"]):
                    role = get(message.guild.roles, id=i["roleId"])
                    if role:
                        if not role in Author.roles:
                            try:
                                await Author.add_roles(role)
                                AddedList.append(role)
                                AddedRoles = AddedRoles+"\n"+role.mention
                            except:
                                pass
                elif int(i["min"]) == 0 and int(role["rank"]) <= int(i["max"]):
                    role = get(message.guild.roles, id=i["roleId"])
                    if role:
                        if not role in Author.roles:
                            try:
                                await Author.add_roles(role)
                                AddedList.append(role)
                                AddedRoles = AddedRoles+"\n"+role.mention
                            except:
                                pass
                else:
                    role = get(message.guild.roles, id=i["roleId"])
                    if role:
                        if role in Author.roles:
                            try:
                                if not role in AddedList:
                                    await Author.remove_roles(role)
                                    RemovedRoles = RemovedRoles+"\n"+role.mention
                            except:
                                pass
            elif int(i["min"]) == 0:
                role = get(message.guild.roles, id=i["roleId"])
                if role:
                    if not role in Author.roles:
                        try:
                            await Author.add_roles(role)
                            AddedList.append(role)
                            AddedRoles = AddedRoles+"\n"+role.mention
                        except:
                                pass

    if len(AddedRoles) < 2:
        AddedRoles = "None"

    if len(RemovedRoles) < 2:
        RemovedRoles = "None"

    try:
        await mainMessage.edit(embed=rolesEmbed(Nickname, AddedRoles, RemovedRoles, Format))
    except:
        pass

    return

async def unbindAccount(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[Username]",
            "command": "unbindaccount",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    ReplyMethod = message.channel.send

    if UserData == None:
        createAuthorData(AuthorId)
        UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    SpecifiedUserData = UserData

    Index = 0
    HasDel = False
    for i in SpecifiedUserData["BoundAccounts"]:
        if i["Username"].lower() == Arguments[1].lower():
            SpecifiedUserData["BoundAccounts"].pop(Index)
            HasDel = True 
        Index += 1

    if HasDel == False:
        await throw("notFound", ReplyMethod)
        return

    UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")
    UserData = SpecifiedUserData
    SaveData(f"./Data/User_Data/{str(AuthorId)}.json", UserData)
    await throw("unbound", ReplyMethod)

async def bindAccount(message, Client):

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    UserData = getData(f"./Data/ServerUser_Data_Data/{str(AuthorId)}.json")

    ReplyMethod = message.channel.send

    if UserData == None:
        createAuthorData(AuthorId)
        UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    SpecifiedUserData = UserData

    await throw("checkDM", message.channel.send)

    dmChannelMethod = await getDM(Author)

    async def userName():

        reply = await executePromptDM(Client, dmChannelMethod.send, bindAccountUser(), message, 60.0)

        if reply == "cancel" or reply == "timeout":
            await throw(reply, dmChannelMethod.send)
            return 200
        else:
            userResponse = requests.get("http://api.roblox.com/users/get-by-username?username="+reply.content)
            if userResponse.status_code == 200:
                b = json.loads(userResponse.text)
                if not "Id" in b:
                    await throw("invalidUser", Method)
                    data = userName()
                    if data == 200:
                        return 200
                    else:
                        return data
                else:
                    return b
            else:
                await throw("apiError", dmChannelMethod.send)
                return 200

    userData = await userName()
    userName = userData["Username"]
    if userData == 200: 
        return

    if not os.path.isfile(f"./WebAPI/VerifyQueue/{userName}.txt"):
        with open(f"./WebAPI/VerifyQueue/{userName}.txt", "a+") as file:
            file.write(json.dumps({
                "discordId": AuthorId,
                "tag": Author.discriminator
            }))
            file.close()
    else:
        await dmChannelMethod.send(embed=discord.Embed(
            title = "Account error",
            description = "An other discord user already seems to try to verify this account, please try binding the account later again with !bindaccount.",
            color = 0xc84c4c,
        ))
        return

    for i in SpecifiedUserData["BoundAccounts"]:
        if i["Username"] == userData["Username"]:
            await throw("userExist", dmChannelMethod.send)
            return

    code = gen()
    await dmChannelMethod.send(embed=bindAccountDone())

    async def getDone():

        reply = await executePromptDM(Client, dmChannelMethod.send, bindAccountDone2(), message, 300.0)

        if reply == "cancel" or reply == "timeout":
            if reply == "timeout":
                if not os.path.isfile(f"./WebAPI/VerifyQueue/{userName}.txt"):
                    await dmChannelMethod.send(embed=discord.Embed(
                        description = "Account has been verified through game.",
                        color = 0x3a9518,
                    ))
                    return 200
            os.remove(f"./WebAPI/VerifyQueue/{userName}.txt")
            await throw(reply, dmChannelMethod.send)
            return 200
        else:
            if reply.content.lower() == "done":
                return "done"
            else:
                data = await getDone()
                if data == 200:
                    return 200
                else:
                    return data

    done = await getDone()
    if done == 200: 
        return
    if not os.path.isfile(f"./WebAPI/VerifyQueue/{userName}.txt"):
        await dmChannelMethod.send(embed=discord.Embed(
            description = "Account has been verified through game.",
            color = 0x3a9518,
        ))
        return

    await dmChannelMethod.send(embed=discord.Embed(
            description = "Account hasn't been verified through game, retry with !bindaccount.",
            color = 0x3a9518,
        ))

    try:
        os.remove(f"./WebAPI/VerifyQueue/{userName}.txt")
    except:
        pass
    return
           