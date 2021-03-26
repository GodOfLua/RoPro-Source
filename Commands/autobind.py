
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

def groupexist(serverid,groupid):
    network = requests.get("https://groups.roblox.com/v1/groups/"+groupid)
    if network.status_code == 200:
        return json.loads(network.text)
    else:
        return "unavailable"

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
            "arguments": "[GroupId]",
            "command": "autobind",
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
        return

    Author = message.author
    Guild = message.guild
    Admin = Author.guild_permissions.administrator
    Role = Discord_Bot.hasModRole(message.author, message.guild)
    AuthorId = str(Author.id)
    RoleId = Role[1]
    HasRole = Role[0]
    role = Role[2]
    GuildId = str(Guild.id)

    UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")
    if UserData == None:
        createAuthorData(AuthorId)
        UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    if RoleId == 0:
        if not Admin:
            await throw("permissionError", {
                "method": message.channel.send,
                "permission": "`ADMINISTRATOR`"
            })
            return
    else:
        if not HasRole:
            await throw("roleError2", {
                "method": message.channel.send,
                "permission": role.mention
            })
            return

    mainMSG = await throw("workingMethod", message.channel.send)

    response = requests.get(f"https://groups.roblox.com/v1/groups/{GroupId}/roles")

    if response.status_code == 400:
        embed.description = "Your specified group dosen't exist"
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
    elif response.status_code != 200:
        await mainMSG.edit(embed=apiError())

    response = json.loads(response.text)
    Embed = discord.Embed(title="Created the following bindings")

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if not GroupId in GuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    for i in response["roles"]:
        role = discord.utils.get(message.guild.roles, name=i["name"])
        r = "False"
        if not role:
            try:
                role = await message.guild.create_role(name=i["name"], hoist=True)
                r = "True"
            except:
                pass
        if role:
            rx = False 
            for x in GuildData["BOUND_GROUPS"][GroupId]["BINDING"]:
                if x["roleId"] == role.id and x["min"] == i["rank"]:
                    rx = True 
                    break 
            if rx == False:
                GuildData["BOUND_GROUPS"][GroupId]["BINDING"].append({
                    "roleId": role.id,
                    "min": i["rank"],
                    "max": i["rank"]
                })
                Embed.add_field(name="Bind for "+role.mention+" ( "+role.name+" )", value="Created role: "+r+"\nRank: "+str(i["rank"]), inline=False)
    
    Embed.color = 0x3a9518
    await mainMSG.edit(embed=Embed)
    SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
            
    

    