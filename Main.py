
# Madee by PrintedScript and GodOf_Lua

from Modules.consoleprint import printi
from Modules.serverprefix import get_prefix,config_prefix
import requests
import time
import json
from colorama import Fore,Back,Style
import discord 
from discord import Embed as Embed
import asyncio
import datetime
import os
import random
from discord.utils import get

# RobloxAPI

from Modules.RobloxAPI.VerificationModule import Verification as VerifyUser
from Modules.RobloxAPI.VerificationModule import *
from Modules.RobloxAPI.RankingModule import *
from Modules.RobloxAPI.User import *
from Modules.Economy.MainEco import *

# Discord 

from Modules.Discord.HelpFormat import *

intents = discord.Intents.default()
intents.members = True
start_time = time.time()

Settings = json.loads(open("./Data/BOT_SETTINGS.json").read())
Token = Settings["TOKEN"]

Client = discord.Client(intents=intents)

async def status():
     while True:
        await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" ! | !invite"))
        await asyncio.sleep(20)
        totalCount = 0
        for i in Client.guilds:
            totalCount += len(i.members)
        await Client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" over "+str(totalCount)+" users"))
        await asyncio.sleep(20)

LastCommand = {}

@Client.event 
async def on_ready():
    printi("Bot has loaded all libraries.",start_time)
    Client.loop.create_task(status())

@Client.event 
async def on_message(message):
    global LastCommand
    if message.author.bot or message.channel.type == discord.ChannelType.private:
        return  


    Server_Prefix = get_prefix(str(message.guild.id))

    if message.content[0:len(Server_Prefix)] == Server_Prefix:
        try:

            Reply = message.channel.send
            if str(message.author.id) in LastCommand:
                TimeDiff = round(time.time() - LastCommand[str(message.author.id)],2)
                if TimeDiff <= 2:
                    await Reply(embed=Embed(
                        title = "Command Cooldown",
                        description = "You are currently on command cooldown. Time remaining: "+str(TimeDiff),
                        color = 0xff0000
                    ))
                    return
            LastCommand[str(message.author.id)] = time.time()
            printi(f"Command called from {str(message.guild.id)}",start_time)

            # Message

            Arguments = message.content.split(" ")
            Command = Arguments[0][len("!"):len(Arguments[0])]
            GuildId = message.guild.id
            Author = message.author
            BackgroundLessColor = int(3553599)

            # Permissions

            IsAdministrator = message.author.guild_permissions.administrator
            canManageRoles = message.author.guild_permissions.manage_roles

            # Methods


            if Command == "cprefix":

                if IsAdministrator:

                    if len(Arguments) == 2:
                        Success = config_prefix(str(message.guild.id), Arguments[1])
                        if Success != True:
                            await Reply(embed=Embed(
                                title = "Unknown Error",
                                description = "Sorry, an error was caught while trying to change the server prefix, error: "+Success,
                                color = 0xff0000
                            ))
                            printi(f"config_prefix caught error: {Fore.RED}{Success}{Style.RESET_ALL}",start_time)
                        else:
                            await Reply(embed=Embed(
                                title = "Server prefix changed",
                                description = "Changed server prefix to: "+Arguments[1],
                                color = 0x00ff2a
                            ))
                            printi(f"{str(message.guild.id)} prefix changed to {Arguments[1]}", start_time)
                    else:
                        await Reply(embed=Embed(
                            title = "Missing arguments",
                            description = "Command 'addgroup' requires 2 arguments, example how to run it: "+Server_Prefix+"cprefix [Prefix]",
                            color = 0xff0000
                        ))  
                else:
                    await Reply(embed=Embed(
                        title = "Permission denied",
                        description = "Missing following permissions to manage server prefix: ADMINISTRATOR",
                        color = 0xff7b00
                    ))
            elif Command == "setverifychannel":
                await setVerifyChannel(message, Arguments)
            elif Command == "setcookie":
                await setcookie(message, Arguments, Client)
            elif Command == "list":
                await listr(message, Arguments)
            elif Command == "valcookie":
                await checkCookie(message, Arguments)
            elif Command == "setnickname":
                await setNickname(message, Arguments)
            elif Command == "promote":
                update = await promote(message, Arguments)
                try:
                    Arguments[2]
                except:
                    return
                member = get(message.guild.members, display_name=Arguments[2])
                if member and canManageRoles and update:
                    await VerifyUser(message, member, Command)
            elif Command == "demote":
                await demote(message, Arguments)
                try:
                    Arguments[2]
                except:
                    return
                member = get(message.guild.members, display_name=Arguments[2])
                if member:
                    await VerifyUser(message, member, Command)
            elif Command == "setrank":
                await setrank(message, Arguments)
                try:
                    Arguments[2]
                except:
                    return
                member = get(message.guild.members, display_name=Arguments[2])
                if member:
                    await VerifyUser(message, member, Command)
            elif Command == "invite":
                await Reply(embed=Embed(
                    title = "Invite our bot!",
                    description = "[Invite me](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot) * [Support Server](https://discord.gg/mrJyPf8NgS)",
                    color = 0x009dff
                ))    

            elif Command == "credits":
                await Reply(embed=Embed(
                    title = "Credits",
                    description = "Made by GodOf_Lua#2643 and SomethingElse#0024",
                    color = 0x009dff
                )) 

            elif Command == "info":
                await Reply(embed=Embed(
                    title = "Bot Info",
                    description = "The bot was made serving the purpose of offering a free roblox API bot for everyone to use.",
                    color = 0x009dff
                )) 

            elif Command == "setup":
                await Reply(embed=Embed(
                    title = "Sent setup",
                    description = "Check your dms! (Make sure your DMs are open.)",
                    color = 0x00ff2a
                )) 
                if message.author.dm_channel:
                    await message.author.dm_channel.send("```css\n[HOW TO SET UP THE BOT]``````diff\n+ Settings up the bot is easily done, all you have to do is to add at least 1 group to the database with the addgroup command. Usage:\naddgroup [GroupId] [Cookie]\n+ The Cookie argument is the .ROBLOSECURITY cookie of your bot. We recommed making another account and take it's cookie to use it to rank people.\n\n``````diff\n- You can check if your cookie expired with the valcookie command. Usage:\nvalcookie [Group Number]\n\n``````diff\n- If the cookie expired you can use the ugroup command to update it. Usage:\nugroup [Group Number] [Cookie]\n\n``````diff-\n To remove a group from the database, including it's cookie you use the removegroup command. Usage:\nremovegroup [Group Number]\n\n``````css\n[All the commands above require Administrator permissions.]\n\n``````css\n[The Group Number is the Id it gets assigned, The Id is always the first number infront of the name in the list of the list command.]\n\n``````css\n[Once you have added 1 group you can begin using the commands: promote,demote,setrank,list and rlist]\n\n``````diff\n- For more information you can run the command help.```")
                else:
                    await message.author.create_dm()
                    await message.author.dm_channel.send("```css\n[HOW TO SET UP THE BOT]``````diff\n+ Settings up the bot is easily done, all you have to do is to add at least 1 group to the database with the addgroup command. Usage:\naddgroup [GroupId] [Cookie]\n+ The Cookie argument is the .ROBLOSECURITY cookie of your bot. We recommed making another account and take it's cookie to use it to rank people.\n\n``````diff\n- You can check if your cookie expired with the valcookie command. Usage:\nvalcookie [Group Number]\n\n``````diff\n- If the cookie expired you can use the ugroup command to update it. Usage:\nugroup [Group Number] [Cookie]\n\n``````diff-\n To remove a group from the database, including it's cookie you use the removegroup command. Usage:\nremovegroup [Group Number]\n\n``````css\n[All the commands above require Administrator permissions.]\n\n``````css\n[The Group Number is the Id it gets assigned, The Id is always the first number infront of the name in the list of the list command.]\n\n``````css\n[Once you have added 1 group you can begin using the commands: promote,demote,setrank,list and rlist]\n\n``````diff\n- For more information you can run the command help.```")

            elif Command == "help":
                if len(Arguments) == 1:
                    embed=discord.Embed(title="Help list", color=0x8000ff, description="More commands will be added in future if you want to keep track of process join our [discord](https://discord.gg/YAjecH3uPx)\nIf you wish to use this bot in your server click [here](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot)")     
                    embed.add_field(name="Verification ", value="run !help verification", inline=True)
                    embed.add_field(name="Ranking", value="run !help ranking", inline=True)
                    embed.add_field(name="Economy", value="run !help economy", inline=True)
                    embed.set_footer(text="Made by GodOf_Lua #2643 and SomethingElse#0024")
                    await Reply(embed=embed)
                else:
                    if Arguments[1].lower() == "verification" or Arguments[1].lower() == "verify":     
                        try:
                            Arguments[2]
                        except:
                            await Reply(embed=helpv())
                            return
                        if Arguments[2] == "2":
                            await Reply(embed=helpv2())
                        else:
                            await Reply(embed=helpv())
                    elif Arguments[1].lower() == "ranking":
                        await Reply(embed=helpr())
                    elif Arguments[1].lower() == "economy" or Arguments[1].lower() == "eco":
                        await Reply(embed=helpe())


            elif Command == "verify":

                from Modules.DataManagement import createAuthorData
                createAuthorData(str(message.author.id))
                with open(f"./Data/User_Data/{str(message.author.id)}.json", "r") as file:
                    Data = json.loads(file.read())
                    file.close()

                if len(Data["BoundAccounts"]) < 1:
                    await bindAccount(message, Client)      
                else:
                    await VerifyUser(message, None, Command)
            elif Command == "getuserinfo":
                await getuserinfo(message, Arguments)
            elif Command == "bindaccount":
                await bindAccount(message, Client)
            elif Command == "unbindaccount":
                await unbindAccount(message, Arguments)
            elif Command == "userlist":
                await userList(message, Arguments)
            elif Command == "bind":
                await bind(message, Arguments)
            elif Command == "unbind":
                await unbind(message, Arguments)
            elif Command == "getroles":
                await VerifyUser(message, None, Command)
            elif Command == "bindings":
                await listBindings(message, Arguments)
            elif Command == "setprimary":
                await setprimary(message, Arguments)
            elif Command == "magicwords":
                await Reply(embed=magicword())
            elif Command == "update":
                try: 
                    if canManageRoles:
                        message.mentions[0]
                        Author = message.mentions[0]
                except:
                    pass
                if len(Arguments) == 2 and Author == message.author and canManageRoles:
                    t = message.guild.get_member(int(Arguments[1]))
                    if t:
                        Author = t 
                    else:
                        await Reply(embed=Embed(
                            description = "Unable to find the user your looking for.",
                            color = BackgroundLessColor,
                        ))
                        return
                await VerifyUser(message, Author, Command)
            #Economy Commands
            elif Command == "bal" or Command == "balance":
                await checkbal(message,Arguments)
            elif Command == "dep" or Command == "deposit":
                await deposit(message,Arguments)
            elif Command == "withdraw":
                await withdraw(message,Arguments)
        except Exception as e:
            import traceback

            printi("Exception occured logged in Error_Logs",start_time)
            ErrorMessage = f'''
/// ERROR START ///
            
    /// INFO START ///
        / MESSAGE ID: {str(message.id)}
        / AUTHOR ID : {str(message.author.id)}
        / GUILD ID  : {str(message.guild.id)}
        / DATETIME  : {datetime.datetime.now()}
    /// INFO END ///

    /// TRACEBACK START ///

{traceback.format_exc()}

    /// TRACEBACK END ///

    /// EXCEPTION START ///

{e}

    /// EXCEPTION END ///

/// ERROR END ///
            '''
            with open(f"./Data/Error_Logs/LOG_{str(round(time.time()))}.LOG","a+") as f:
                f.write(ErrorMessage)
    
Client.run(Token)