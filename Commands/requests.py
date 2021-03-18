
import json 
import asyncio 
import discord 
import requests
from discord.utils import get
from Modules.Discord.Embeds import *
from Modules.DataManagement import *

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
            "arguments": "<GroupId> <OPTIONAL: PAGE>",
            "command": "requests",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    ReplyMethod = message.channel.send

    if not Arguments[1].isnumeric():
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })
        return

    Admin = Author.guild_permissions.administrator

    if not Admin:
        await throw("permissionError", {
            "method": message.channel.send,
            "permission": "`ADMINISTRATOR`"
        })
        return

    mainMSG = await throw("workingMethod", ReplyMethod)

    if GuildData == None:
        createGuildData(GuildId)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    GroupId = Arguments[1]

    if not GroupId in GuildData["BOUND_GROUPS"]:
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")
        GuildData["BOUND_GROUPS"][GroupId] = {
            "ID": GroupId,
            "BINDING": [],
            "COOKIE": "NONE",
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", GuildData)
        GuildData = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    verCookie = valCookie(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])
    x_csrf_token = get_x_csrf_token(GuildData["BOUND_GROUPS"][GroupId]["COOKIE"])

    embed = discord.Embed()
    embed.set_footer(text="Powered by RoPro System · !invite")

    if verCookie != 200:
        embed.description = "API error or invalid cookie."
        embed.color = 0xc84c4c
        await mainMSG.edit(embed=embed)
        return

    page = 1
    try:
        Arguments[2]
        if Arguments[2].isnumeric():
            page = int(Arguments[2])
    except:
        pass

    currentPage = 0
    cursor = "none"

    for i in range(page):
        currentPage = i+1
        if cursor == None:
            embed.description = "Nothing to see here!"
            embed.color = 0xc337ac
            await mainMSG.edit(embed=embed)
            break
        if cursor != "none":
            res = requests.get(f"https://groups.roblox.com/v1/groups/{GroupId}/join-requests?limit=10&cursor"+cursor, headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]})
        else:
            res = requests.get(f"https://groups.roblox.com/v1/groups/{GroupId}/join-requests?limit=10", headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": GuildData["BOUND_GROUPS"][GroupId]["COOKIE"]})
        if res.status_code == 200:
            res = json.loads(res.text)
            try:
                res["data"][0]
                if currentPage != page:
                    if res["nextPageCursor"] != "none":
                        cursor = res["nextPageCursor"]
                else:
                    if currentPage != page:
                        embed.description = "Nothing to see here!"
                        embed.color = 0xc337ac
                        await mainMSG.edit(embed=embed)
                        break
                    index = 0
                    for x in res["data"]:
                        embed.add_field(name="Join request #"+str(index+1), value="Username: "+x["requester"]["username"]+"\nUserId: "+str(x["requester"]["userId"]))
                        embed.set_footer(text="Say !requests [GroupId] "+str(page+1) + " to see the next page | Powered by RoPro System")
                        embed.description = "Run !accept or !decline to change a user request state."
                        embed.color = 0xc337ac
                        index += 1
                    await mainMSG.edit(embed=embed)
            except:
                embed.description = "Nothing to see here!"
                embed.color = 0xc337ac
                await mainMSG.edit(embed=embed)
                break
        else:
            await mainMSG.edit(embed=apiError())
            break

