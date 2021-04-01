
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
    unverifiedRole = get(message.guild.roles, id=GuildData["UnverifiedRole"])

    if unverifiedRole:
        if unverifiedRole in Author.roles:
            try:
                await Author.remove_roles(unverifiedRole)
                RemovedRoles = RemovedRoles+unverifiedRole.mention
            except:
                pass
    
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
           