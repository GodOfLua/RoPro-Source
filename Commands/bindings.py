
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

async def run(message, Arguments, Client, Discord_Bot):

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