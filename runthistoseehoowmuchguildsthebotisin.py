
# Madee by PrintedScript and GodOf_Lua

import discord 
from discord.utils import get


# RobloxAPI
import json

intents = discord.Intents.default()
intents.members = True

Settings = json.loads(open("./Data/BOT_SETTINGS.json").read())
Token = Settings["TOKEN"]

Client = discord.Client(intents=intents)

@Client.event 
async def on_ready():
    print(list(Client.guilds))
    print(len(list(Client.guilds)))
    g = get(Client.guilds, id=707592892251766914)
    x = get(g.channels, id=814975639836164137)
    #await x.send('''```
#-> Added setverifychannel command, makes the bot only react to the specified channel
#-> Updated help
#-> You can now make multiple binds for 1 role.
##-> Bindings command can now list more bindings.
#-> Bot dosen't force update anymore if rank didn't got changed.
#-> Restricted update command to update other users
#-> Added setprimary command, it's used to specify the priortized group in setting the nicknname of a user. (This is only important if your format uses {role})
#-> Added setnickname command, you use it to set the nickname format that people get their nickname given with
#-> Help has now multiple pages
#-> Updated getroles response.
#-> Removed the option to verify by putting a code in your status/about as it confused people.

#Date: 06/03/2021```
#|| @everyone ||
    #''')

Client.run("ODEwNDc4NDQxMjI0NzMyNzAy.YCkO3g.wh8fcXgXtdbbQW8PvSXfhcpKrWw")