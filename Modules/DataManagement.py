
import json 
import os

def getData(path):
    if os.path.isfile(path):
        with open(path, "r") as file:
            fileString = file.read()
            filePayloadString = json.loads(fileString)
            file.close()
            return filePayloadString
    else:
        return None

def SaveData(path, payload):

    if os.path.isfile(path):
        with open(path, "w") as file:
            payloadString = json.dumps(payload)
            file.write(payloadString)
            file.close()
    else:
        with open(path, "a+") as file:
            payloadString = json.dumps(payload)
            file.write(payloadString)
            file.close()

def createGuildData(GuildId):

    if not os.path.isfile(f"./Data/Server_Data/{str(GuildId)}.json"):
        Data = {
            "SERVER_PREFIX": "!",
            "GROUPS": {},
            "BOUND_GROUPS": {},
            "RoNick": True,
            "VerifyChannel": "none",
            "NicknameFormat": "{roblox_name}",
            "Acronyms": {},
        }
        SaveData(f"./Data/Server_Data/{str(GuildId)}.json", Data)

def createAuthorData(AuthorId):

    if not os.path.isfile(f"./Data/User_Data/{str(AuthorId)}.json"):
        Data = {
            "BoundAccounts": [],
            "SelectedAccountIndex": 0,
        }
        SaveData(f"./Data/User_Data/{str(AuthorId)}.json", Data)

def putRoNick(GuildId):

    Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Data == None:
        createGuildData(GuildId)
        Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
    Data["RoNick"] = True
    SaveData(f"./Data/Server_Data/{GuildId}.json", Data)

def putVerify(GuildId):

    Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Data == None:
        createGuildData(GuildId)
        Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
    Data["VerifyChannel"] = "none"
    SaveData(f"./Data/Server_Data/{GuildId}.json", Data)

def putnickformat(GuildId):

    Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Data == None:
        createGuildData(GuildId)
        Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
    Data["NicknameFormat"] = "{roblox_name}"
    SaveData(f"./Data/Server_Data/{GuildId}.json", Data)

def putprimary(GuildId):

    Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Data == None:
        createGuildData(GuildId)
        Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
    Data["PrimaryNickname"] = "none"
    SaveData(f"./Data/Server_Data/{GuildId}.json", Data)

def putAcronyms(GuildId):

    Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Data == None:
        createGuildData(GuildId)
        Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
    Data["Acronyms"] = {}
    SaveData(f"./Data/Server_Data/{GuildId}.json", Data)

def putModRole(GuildId):

    Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")

    if Data == None:
        createGuildData(GuildId)
        Data = getData(f"./Data/Server_Data/{str(GuildId)}.json")
    
    Data["modrole"] = 0
    SaveData(f"./Data/Server_Data/{GuildId}.json", Data)