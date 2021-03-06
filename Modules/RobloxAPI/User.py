
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
import datetime

async def getuserinfo(message, Arguments):
    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[Username]",
            "command": "getuserinfo",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    r = requests.get(url=f"https://api.roblox.com/users/get-by-username?username={Arguments[1]}")
    if r.status_code == 200:
        if 'sucess' not in r.json() and 'Id' in r.json():
            Player_ID = str(r.json()["Id"])
            STAN_User_API = requests.get(url=f"https://users.roblox.com/v1/users/{Player_ID}")
            if STAN_User_API.status_code == 200:
                TempDataStore = {}
                STANJSON = STAN_User_API.json()
                TempDataStore["Username"] = STANJSON["name"]
                TempDataStore["displayName"] = STANJSON["displayName"]
                TempDataStore["description"] = STANJSON["description"]
                TempDataStore["created"] = STANJSON["created"]
                TempDataStore["id"] = STANJSON["id"]
                TempDataStore["IsOnline"] = r.json()["IsOnline"]
                DATETIME_R = datetime.datetime.now()
                Target_User_Data = {
                    "$Archive_Datetime":DATETIME_R,
                    "Archived_Data":TempDataStore
                }
                embed=discord.Embed(title=TempDataStore["Username"], description=TempDataStore["description"], color=0x8000ff)
                embed.add_field(name="Display Name", value=TempDataStore["displayName"], inline=False)
                embed.add_field(name="Creation Date", value=TempDataStore["created"], inline=False)
                embed.add_field(name="Player ID", value=TempDataStore["id"], inline=False)
                embed.add_field(name="Online", value=TempDataStore["IsOnline"], inline=False)
                embed.set_footer(text="Powered by RoPro Verification System · !invite")
                await message.channel.send(embed=embed)

                if os.path.isfile(f"./Data/User_Archives/{Player_ID}.json"):
                    with open(f"./Data/User_Archives/{Player_ID}.json","w") as f:
                        json.dump(Target_User_Data,f,sort_keys=True,default=str)
                else:
                    with open(f"./Data/User_Archives/{Player_ID}.json","a+") as f:
                        json.dump(Target_User_Data,f,sort_keys=True,default=str)
            elif STAN_User_API.status_code == 404:
                if os.path.isfile(f"./Data/User_Archives/{Player_ID}.json"):
                    printi(f"Found old archive of {Player_ID}",start_time)
                    with open(f"./Data/User_Archives/{Player_ID}.json","r") as f:
                        OLD_Archived_Data = json.load(f)
                    await message.channel.send(embed=Embed(
                        title = "Archived Profile",
                        description = f"The information below is old as the account is banned. Archive Date: "+OLD_Archived_Data["$Archive_Datetime"],
                        color = 0xff7300
                    ))
                    TempDataStore = OLD_Archived_Data["Archived_Data"]
                    embed=discord.Embed(title=TempDataStore["Username"], description=TempDataStore["description"], color=0x8000ff)
                    embed.add_field(name="Display Name", value=TempDataStore["displayName"], inline=False)
                    embed.add_field(name="Creation Date", value=TempDataStore["created"], inline=False)
                    embed.add_field(name="Player ID", value=TempDataStore["id"], inline=False)
                    embed.add_field(name="Online", value=TempDataStore["IsOnline"], inline=False)
                    embed.set_footer(text="Powered by RoPro Verification System · !invite")
                    await message.channel.send(embed=embed)
                else:
                    await message.channel.send(embed=Embed(
                        title = "Player is banned",
                        description = "The account is currently banned which does not allow us to view it, there is also no archive in our database of this user.",
                        color = 0xff0000
                    )) 
        else:
            await message.channel.send(embed=Embed(
                title = "Player not found",
                description = "Roblox has returned 404.",
                color = 0xff0000
            )) 

async def listr(message, Arguments):

    if len(Arguments) < 2:
        await throw("argumentError", {
            "method": message.channel.send,
            "arguments": "[GroupId]",
            "command": "list",
            "length": 1,
            "pronounce": "Argument"
        })
        return

    if Arguments[1].isnumeric():

        embed = discord.Embed()
        embed.set_footer(text="Powered by RoPro Verification System · !invite")

        d = requests.get("https://groups.roblox.com/v1/groups/"+str(Arguments[1])+"/roles")
        if d.status_code == 200:
            d = json.loads(d.text)
            Text = ""
            for i in d["roles"]:
                Text = Text +"\n\nRole: "+i["name"]+"\nRank: "+str(i["rank"])
            embed.description = Text
            embed.color = 0xc337ac
            await message.channel.send(embed=embed)
        else:
            embed.description = "API error or invalid group Id."
            embed.color = 0xc84c4c
            await message.channel.send(embed=embed)
            return
    else:
        await throw("numericError", {
            "method": message.channel.send,
            "nameofError": "GroupId"
        })

async def userList(message, arguments):

    embed = discord.Embed(color=0xc337ac)
    embed.set_footer(text="Powered by RoPro Verification System · !invite")

    Author = message.author
    Guild = message.guild

    GuildId = str(Guild.id)
    AuthorId = str(Author.id)

    UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    ReplyMethod = message.channel.send

    if UserData == None:
        createAuthorData(AuthorId)
        UserData = getData(f"./Data/User_Data/{str(AuthorId)}.json")

    if len(UserData["BoundAccounts"]) < 1:
        embed.description = "No accounts are asssociated with this discord account."
        await ReplyMethod(embed=embed)
        return

    Text = ""
    for i in UserData["BoundAccounts"]:
        Text = Text +"\n\n"+i["Username"]+","

    embed.title = "Associated Accounts"
    embed.description = Text 
    await ReplyMethod(embed=embed)
    return
                