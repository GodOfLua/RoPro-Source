from Modules.DataManagement import *

def get_prefix(serverId):

    PrefixData = getData(f"./Data/Server_Data/{str(serverId)}.json")
    if PrefixData == None:
        createGuildData(serverId)
        PrefixData = getData(f"./Data/Server_Data/{str(serverId)}.json")
    return PrefixData["SERVER_PREFIX"]

def config_prefix(serverId, newPrefix):

    PrefixData = getData(f"./Data/Server_Data/{str(serverId)}.json")
    if PrefixData == None:
        createGuildData(serverId)
        PrefixData = getData(f"./Data/Server_Data/{str(serverId)}.json")
    PrefixData["SERVER_PREFIX"] = newPrefix

    SaveData(f"./Data/Server_Data/{str(serverId)}.json",PrefixData)