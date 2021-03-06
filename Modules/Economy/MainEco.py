# Main economy file written by SomethingElse#0024 and GodOf_Lua#2643
from Modules.Discord.Embeds import *
from Modules.DataManagement import *
import discord 

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