
from discord.utils import get 

def getRole(roleP, roleList, msg):

    role = None 

    try:
        msg.role_mentions[0]
        role = msg.role_mentions[0]
        return role 
    except: 
        pass 

    if roleP.isnumeric():
        roleB = get(roleList, id=roleP)
        if roleB:
            role = roleB

    if not role:
        roleB = get(roleList, name=roleP)
        if roleB:
            role = roleB

    return role