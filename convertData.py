from Modules.DataManagement import *
import os
import json 

d = getData("./Data/Server_Data/GUILD_DATA.json")

ind = 0
for i in d:
    key = list(d.keys())[ind]
    if not os.path.isfile(f"./Data/Server_Data/{str(key)}.json"):
        with open(f"./Data/Server_Data/{str(key)}.json", "a+") as file:
            i = d[i]
            print(i)
            data = json.dumps(i)
            file.write(data)
            file.close()
    ind+=1