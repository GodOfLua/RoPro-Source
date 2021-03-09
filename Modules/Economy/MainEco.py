# Main economy file written by SomethingElse#0024 and GodOf_Lua#2643
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
import discord 
import time
import random

FooterText = "Powered by RoPro System · !invite"

def GetUserEconomyData(id):
    AuthorData = getData(f"./Data/UserEconomy_Data/{str(id)}.json")
    if AuthorData == None:
        DefaultData = {
            "cashvalue" : {
                "wallet" : 0,
                "bank" : 0
            },
            "inventory" : {},
            "lastredeem" : {
                "day" : {
                    "unix" : 0,
                },
                "weekly" : {
                    "unix" : 0,
                },
                "monthly" : {
                    "unix" : 0,
                },
            }
        }
        SaveData(f"./Data/UserEconomy_Data/{str(id)}.json",DefaultData)
        AuthorData = getData(f"./Data/UserEconomy_Data/{str(id)}.json")
    return AuthorData

def CheckCooldown(Command,id):
    CooldownCache = getData(f"./Modules/Economy/CooldownCache/{str(id)}.json")
    if CooldownCache == None:
        DefaultData = {}
        SaveData(f"./Modules/Economy/CooldownCache/{str(id)}.json",DefaultData)
        CooldownCache = getData(f"./Modules/Economy/CooldownCache/{str(id)}.json")
    if Command in CooldownCache:
        return CooldownCache[Command]
    else:
        return 0

def SaveCooldown(Command,id):
    CooldownCache = getData(f"./Modules/Economy/CooldownCache/{str(id)}.json")
    if CooldownCache == None:
        DefaultData = {}
        SaveData(f"./Modules/Economy/CooldownCache/{str(id)}.json",DefaultData)
        CooldownCache = getData(f"./Modules/Economy/CooldownCache/{str(id)}.json")
    CooldownCache[Command] = time.time()
    SaveData(f"./Modules/Economy/CooldownCache/{str(id)}.json",CooldownCache)

async def checkbal(message, Arguments):
    Reply = message.channel.send
    GuildId = message.guild.id
    Author = message.author
    BackgroundLessColor = int(3553599)

    IsAdministrator = message.author.guild_permissions.administrator
    canManageRoles = message.author.guild_permissions.manage_roles

    AuthorData = GetUserEconomyData(Author.id)
    
    WalletCash = AuthorData["cashvalue"]["wallet"]
    BankCash = AuthorData["cashvalue"]["bank"]

    embed=discord.Embed(title="Account balance", description=f"<@{str(Author.id)}> \nWallet : `${str(WalletCash)}` \nBank : `${str(BankCash)}`", color=0x8000ff)
    embed.set_footer(text=FooterText)
    await Reply(embed=embed)
    return

async def deposit(message,Arguments):
    Reply = message.channel.send
    GuildId = message.guild.id
    Author = message.author
    BackgroundLessColor = int(3553599)

    IsAdministrator = message.author.guild_permissions.administrator
    canManageRoles = message.author.guild_permissions.manage_roles

    AuthorData = GetUserEconomyData(Author.id)

    if len(Arguments) >= 2:
        # Checks if all money to deposit
        MoneyTransfer = None
        if Arguments[1] == "all":
            MoneyTransfer = AuthorData["cashvalue"]["wallet"]
        else:
            try:
                MoneyTransfer = int(Arguments[1])
            except:
                await throw("numericError",{"method":Reply,"nameofError":"`Amount`"})
                return
        # Checks if there is enough to deposit
        MoneyDiff = AuthorData["cashvalue"]["wallet"] - MoneyTransfer
        if MoneyDiff < 0:
            embed=discord.Embed(title="Insufficient Account balance", description=f"<@{str(Author.id)}> \nYou do not have enough money to deposit.", color=0xc84c4c)
            embed.set_footer(text=FooterText)
            await Reply(embed=embed)
        else:
            # Updates authordata
            AuthorData["cashvalue"]["bank"] = AuthorData["cashvalue"]["bank"] + MoneyTransfer
            AuthorData["cashvalue"]["wallet"] = AuthorData["cashvalue"]["wallet"] - MoneyTransfer
            SaveData(f"./Data/UserEconomy_Data/{str(Author.id)}.json",AuthorData)

            embed=discord.Embed(title="Money deposited", description=f"<@{str(Author.id)}> \n`${str(MoneyTransfer)}` has been deposited.", color=0x3a9518)
            embed.set_footer(text=FooterText)
            await Reply(embed=embed)
    else:
        await throw("argumentError",{"method":Reply,"command":"deposit","length":1,"pronounce":"Argument","arguments":"[Amount]"})

async def withdraw(message,Arguments):
    Reply = message.channel.send
    GuildId = message.guild.id
    Author = message.author
    BackgroundLessColor = int(3553599)

    IsAdministrator = message.author.guild_permissions.administrator
    canManageRoles = message.author.guild_permissions.manage_roles

    AuthorData = GetUserEconomyData(Author.id)

    if len(Arguments) >= 2:
        # Checks if all money to withdraw
        MoneyTransfer = None
        if Arguments[1] == "all":
            MoneyTransfer = AuthorData["cashvalue"]["bank"]
        else:
            try:
                MoneyTransfer = int(Arguments[1])
            except:
                await throw("numericError",{"method":Reply,"nameofError":"`Amount`"})
                return
        # Checks if there is enough to withdraw
        MoneyDiff = AuthorData["cashvalue"]["bank"] - MoneyTransfer
        if MoneyDiff < 0:
            embed=discord.Embed(title="Insufficient Account balance", description=f"<@{str(Author.id)}> \nYou do not have enough money to withdraw.", color=0xc84c4c)
            embed.set_footer(text=FooterText)
            await Reply(embed=embed)
        else:
            # Updates authordata
            AuthorData["cashvalue"]["bank"] = AuthorData["cashvalue"]["bank"] - MoneyTransfer
            AuthorData["cashvalue"]["wallet"] = AuthorData["cashvalue"]["wallet"] + MoneyTransfer
            SaveData(f"./Data/UserEconomy_Data/{str(Author.id)}.json",AuthorData)

            embed=discord.Embed(title="Money withdrawn", description=f"<@{str(Author.id)}> \n`${str(MoneyTransfer)}` has been withdrawn.", color=0x3a9518)
            embed.set_footer(text=FooterText)
            await Reply(embed=embed)
    else:
        await throw("argumentError",{"method":Reply,"command":"withdraw","length":1,"pronounce":"Argument","arguments":"[Amount]"})

async def beg(message,Arguments):
    Reply = message.channel.send
    GuildId = message.guild.id
    Author = message.author
    BackgroundLessColor = int(3553599)

    IsAdministrator = message.author.guild_permissions.administrator
    canManageRoles = message.author.guild_permissions.manage_roles

    AuthorData = GetUserEconomyData(Author.id)

    Recieve_Custom_Messages = [
        "{Ping}, you found `{Amount}` on the street!",
        "{Ping}, you recieved `{Amount}` from a random stranger.",
    ]

    Failed_Custom_Messages = [
        "{Ping}, someone just told you to go work for your own money.",
    ]
    LastRun = CheckCooldown("beg",Author.id)
    if time.time() - LastRun <= 120:
        TimeLeft = round((120 + LastRun)-time.time(),1)
        await Reply(embed=discord.Embed(
            title = "Command cooldown",
            description = f"You cannot run this command. Time left: `{str(TimeLeft)}s`",
            color = 0xc84c4c
        ))
        return
    else:
        # Chance for getting money 2/3
        # Chance for not getting money 1/3
        if random.randint(1,3) == 2:
            #unlucky
            RandomString = random.choice(Failed_Custom_Messages).format(Ping=f"<@{str(Author.id)}>")
            await Reply(RandomString)
            SaveCooldown("beg",Author.id)
        else:
            ValueAmount = random.randint(70,160)
            RandomString = random.choice(Recieve_Custom_Messages).format(Ping=f"<@{str(Author.id)}>",Amount=f"${str(ValueAmount)}")
            await Reply(RandomString)

            AuthorData["cashvalue"]["wallet"] = AuthorData["cashvalue"]["wallet"] + ValueAmount

            SaveData(f"./Data/UserEconomy_Data/{str(Author.id)}.json",AuthorData)

async def Payment(message,Arguments):
    Reply = message.channel.send
    GuildId = message.guild.id
    Author = message.author
    BackgroundLessColor = int(3553599)

    IsAdministrator = message.author.guild_permissions.administrator
    canManageRoles = message.author.guild_permissions.manage_roles

    AuthorData = GetUserEconomyData(Author.id)
    if len(Arguments) >= 3:
        if "<@!" in message.content and ">" in message.content:
            SplittedMsg1 = message.content.split("<@!")
            SplittedMsg = SplittedMsg1[1].split(">")
            TargetID = SplittedMsg[0]
            TargetUserData = GetUserEconomyData(TargetID)
            MoneyTransfer = None
            try:
                if len(Arguments) >= 4:
                    if Arguments[3] == "all":
                        MoneyTransfer = AuthorData["cashvalue"]["bank"]
                    else:
                        MoneyTransfer = int(Arguments[3])
                else:
                    if Arguments[2] == "all":
                        MoneyTransfer = AuthorData["cashvalue"]["bank"]
                    else:
                        MoneyTransfer = int(Arguments[2])
            except Exception as e:
                await throw("numericError",{"method":Reply,"nameofError":"`Amount`"})
                print(e)
                return
            
            if AuthorData["cashvalue"]["bank"] - MoneyTransfer < 0:
                embed=discord.Embed(title="Insufficient Account balance", description=f"<@{str(Author.id)}> \nYou do not have enough money in your bank to give.", color=0xc84c4c)
                embed.set_footer(text=FooterText)
                await Reply(embed=embed)
            else:
                AuthorData["cashvalue"]["bank"] = AuthorData["cashvalue"]["bank"] - MoneyTransfer
                TargetUserData["cashvalue"]["bank"] = TargetUserData["cashvalue"]["bank"] + MoneyTransfer
                embed=discord.Embed(title="Money transferred", description=f"<@{str(Author.id)}> \n`${str(MoneyTransfer)}` has been transferred to <@!{str(TargetID)}>.", color=0x3a9518)
                embed.set_footer(text=FooterText)
                await Reply(embed=embed)
                SaveData(f"./Data/UserEconomy_Data/{str(Author.id)}.json",AuthorData)
                SaveData(f"./Data/UserEconomy_Data/{str(TargetID)}.json",TargetUserData)
        else:
            await throw("argumentError",{"method":Reply,"command":"pay","length":1,"pronounce":"Argument","arguments":"[Ping] [Amount]"})
    else:
        await throw("argumentError",{"method":Reply,"command":"pay","length":1,"pronounce":"Argument","arguments":"[Ping] [Amount]"})