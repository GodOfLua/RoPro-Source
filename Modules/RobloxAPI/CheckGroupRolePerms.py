import discord
import json
import requests
from Modules.RobloxAPI.GetGroupRole import *

#Guide:
# "permissions": {
#     "groupPostsPermissions": {
#       "viewWall": true,
#       "postToWall": true,
#       "deleteFromWall": true,
#       "viewStatus": true,
#       "postToStatus": true
#     },
#     "groupMembershipPermissions": {
#       "changeRank": true,
#       "inviteMembers": true,
#       "removeMembers": true
#     },
#     "groupManagementPermissions": {
#       "manageRelationships": true,
#       "manageClan": true,
#       "viewAuditLogs": true
#     },
#     "groupEconomyPermissions": {
#       "spendGroupFunds": true,
#       "advertiseGroup": true,
#       "createItems": true,
#       "manageItems": true,
#       "addGroupPlaces": true,
#       "manageGroupGames": true,
#       "viewGroupPayouts": false
#     }


def checkPostsPermissions(groupId, userId):
    roleId = GetGroupRole(groupId, userId)["id"]
    print(roleId)
    #network = requests.get("https://groups.roblox.com/v1/groups/"+str(groupId)+"/roles/")

checkPostsPermissions("10207643","79641334")
#def checkMembershipPermissions(groupId, userId):


#def checkManagementPermissions(groupId, userId):


#def checkEconomyPermissions(groupId, userId):