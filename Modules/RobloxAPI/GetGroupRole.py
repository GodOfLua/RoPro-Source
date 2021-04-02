import discord
import json
import requests

def GetGroupRole(groupId, userId):
    network = requests.get("https://groups.roblox.com/v1/users/"+str(userId)+"/groups/roles")
    if network.status_code == 200:
        responce = json.loads(network.text)
        for i in responce["data"]:
            if i["group"]["id"] == int(groupId):
                print(i["role"])
                return i["role"]
                #print(i["group"]+i["role"])
            #print(i["group"]["name"])
        #print(responce)
    else:
        print("Error happened")
        print(network.status_code)
        return False

GetGroupRole("10207643","79641334")