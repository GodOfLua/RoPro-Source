import discord

def helpv():
    embed=discord.Embed(title="Verification Module commands", description='''

    User commands:

    `verify`    **->**      Verifys an user if no account was bound, you will be prompted to verify your account.
    `getroles`  **->**      Get's roles depending on the rank in group.
    `update <OPTIONAL: UserMention | UserId>`     **->**      Forces update on a user depending on his group rank.
    `userlist`      **->**      Responds with an list of bound accounts.
    `bindaccount`   **->**      Prompts you with the bind account process.
    `unbindaccount <USERNAME>`      **->**      Unbinds an account by the given username.

    Configuration commands:

    `bind <GroupId> <RankRange> <RoleMention | RoleId | RoleName>`     **->**       Binds an rank to an specific role.
    `unbind <GroupId> <RoleMention | RoleId | RoleName>`        **->**      Unbinds an rank from an specific role. (ROLE MUST EXIST)
    `bindings <OPTIONAL: GroupId>`        **->**      Responds with all bindings from the guild/group.
    `magicwords`    **->**  Responds with an list of magic words able to be used in the nickname command.

    Costumization commands:

    `setnickname <StringFormat>`   **->**  Changes the format users gets their username assigned default is {roblox_name} view !magicwords to see all of them.
    `setprimary`<GroupId>`  **->**  Changes the group the bot focuses on when setting a username of a user. (This is only important if you use {role} magic word.)

    Total verifcation module commands: 16

    More commands will be added in future if you want to keep track of process join our [discord](https://discord.gg/dNGrZAPgFY)
    If you wish to use this bot in your server click [here](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot)

    This is page 1 say !help verification 2 to see the next page.
    ''', color=0x8000ff)  
    embed.set_footer(text="Made by GodOf_Lua #2643 and SomethingElse#0024")
    return embed

def helpv2():
    embed=discord.Embed(title="Verification Module commands", description='''

    Costumization commands:

    `setverifychannel <ChannelMention | ChannelId | ChannelName or say none>`   **->**  Changes the verify channel to the specified one. Say none to make the bot respond to the commands verify and getroles in every channel. Specify one to make the bot respond to the commands verify and getroles in the specified one. 

    Acronym commands:

    `addacronym <StringFormat (Example: Level - 1:L1)`  **->**  Adds an acronym to the server settings. An name would be displayed as the acronym instead.
    `delacronym <String (Example: Level - 1)>`  **->**  Removes an acronym from the server settings. Names will stop being displayed as the acronym.
    `acronyms`  **->**  Responds with an list of all set acronyms.

    Explanations:

    `RankRange`     **->**      As example 0:255 which would specify a minimum of rank required 0 and maximum able to get the role 255. You can also just said one number this will be then the min and max at the same time, which means only that rank would get the role.
    `StringFormat`  **->**      An specific format you set. Examples: {role} | {roblox_name}, {roblox_name}

    Total verifcation module commands: 16

    More commands will be added in future if you want to keep track of process join our [discord](https://discord.gg/dNGrZAPgFY)
    If you wish to use this bot in your server click [here](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot)

    This is page 2 say !help verification to see the previous page.
    ''', color=0x8000ff)  
    embed.set_footer(text="Made by GodOf_Lua #2643 and SomethingElse#0024")
    return embed

def helpr():
    embed=discord.Embed(title="Ranking Module commands", description='''
    User commands:

    `list <GroupId>`    **->**      Responds with all roles from a group..

    Configuration commands:

    `setcookie <GroupId>`       **->**      Prompts you to enter the bot cookie used for ranking. (IT'S RECOMMENDED TO MAKE AN SEPERATE ROBLOX ACCOUNT FOR THAT PURPOSE.)
    
    Group commands:

    `promote <GroupId> <Username>`      **->**      Promotes an user to the next higher role in the given group.
    `demote <GroupId> <Username>`      **->**      Demotets an user to the next lower role in the given group.
    `setrank <GroupId> <Username> <Rank>`      **->**      Changes the rank from an user to the specified one..

    More commands will be added in future if you want to keep track of process join our [discord](https://discord.gg/dNGrZAPgFY)
    If you wish to use this bot in your server click [here](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot)
    ''', color=0x8000ff)  
    embed.set_footer(text="Made by GodOf_Lua #2643 and SomethingElse#0024")
    return embed

def helpe():
    embed=discord.Embed(title="Economy Module commands", description='''
    User commands:

    Coming soon.

    More commands will be added in future if you want to keep track of process join our [discord](https://discord.gg/dNGrZAPgFY)
    If you wish to use this bot in your server click [here](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot)
    ''', color=0x8000ff)  
    embed.set_footer(text="Made by GodOf_Lua #2643 and SomethingElse#0024")
    return embed

def magicword():
    embed=discord.Embed(title="Magic Words", description='''

    `{roblox_name}`     **->**  Specifies the roblox username of an user.
    `{role}`     **->**  Specifies the group role of an user.
    `{discord_name}`     **->**  Specifies the discord name of an user.
    `{discord_tag}`     **->**  Specifies the discord tag of an user.

    If you want to keep track of process join our [discord](https://discord.gg/dNGrZAPgFY)
    If you wish to use this bot in your server click [here](https://discord.com/api/oauth2/authorize?client_id=810478441224732702&permissions=8&scope=bot)
    ''', color=0x8000ff)  
    embed.set_footer(text="Made by GodOf_Lua #2643 and SomethingElse#0024")
    return embed
