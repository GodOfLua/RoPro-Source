import flask
from flask import request, jsonify
from flask import Flask, render_template
from flask import Response
import os,sys
import json 
from flask_swagger_ui import get_swaggerui_blueprint
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def groupexist(serverid,groupid):
    network = requests.get("https://groups.roblox.com/v1/groups/"+groupid)
    if network.status_code == 200:
        return json.loads(network.text)
    else:
        return "unavailable"

def get_x_csrf_token(ROBLOSECURITY):
    try:
        token_request = requests.session()
        token_request.cookies['.ROBLOSECURITY'] = ROBLOSECURITY
        r = token_request.post('https://auth.roblox.com/v2/login')
        if r.headers["X-CSRF-TOKEN"] != None:
            return r.headers["X-CSRF-TOKEN"]
        else:
            return None
    except:
        return None

def valCookie(cookie):
    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        network = requests.get("https://api.roblox.com/currency/balance", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        return network.status_code
    else:
        return "Unable to fetch X_CSRF_TOKEN"

SWAGGER_URL = '/docs'
API_URL = '/static/apiDocs.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "RoPro API Documentation"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route('/api/v1/registerRobloxAccount', methods=['POST'])
def api_verify():
    data = request.args 
    print(data)
    
    if not "id" in data or not "username" in data or not "discordId" in data or not "key" in data:
        return Response('{"status": "invalid"}', status=400, mimetype='application/json')

    if data["key"] != "AUTH-cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e":
        return Response('{"status": "auth fail"}', status=403, mimetype='application/json')

    ID = data["id"]
    Username = data["username"]
    DiscordId = data["discordId"]

    if not os.path.isfile(f"./VerifyQueue/{Username}.txt"):
        return Response('{"status": "invalid"}', status=400, mimetype='application/json')

    with open(f"./VerifyQueue/{Username}.txt", "r") as file:
        d = file.read()
        d = json.loads(d)
        DiscordId = d["discordId"]

    if not os.path.isfile(f"../Data/User_Data/{DiscordId}.json"):
        with open(f"../Data/User_Data/{DiscordId}.json", "a+") as file:
            file.write(json.dumps({
                "BoundAccounts": [],
                "SelectedAccountIndex": 0,
            }))
            file.close()
    
    with open(f"../Data/User_Data/{DiscordId}.json", "r") as file:
        data = json.loads(file.read())
    for i in data["BoundAccounts"]:
        if i["Username"] == Username:
            return Response('{"status": "invalid"}', status=400, mimetype='application/json')

    data["BoundAccounts"].append({
        "Username": Username,
        "Id": ID
    })
    with open(f"../Data/User_Data/{DiscordId}.json", "w") as file:
        file.write(json.dumps(data))
    os.remove(f"./VerifyQueue/{Username}.txt")

    return Response('{"status": "success"}', status=200, mimetype='application/json') 

@app.route('/api/v1/data', methods=['GET', 'POST'])
def api_data():
    data = request.args 

    if not "username" in data or not "key" in data:
        return Response('{"status": "invalid"}', status=403, mimetype='application/json')

    if data["key"] != "AUTH-cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e":
        return Response('{"status": "auth fail"}', status=403, mimetype='application/json')
    
    username = data["username"]

    if not os.path.isfile(f"./VerifyQueue/{username}.txt"):
        return Response('{"status": "not_found", "Found": "false"}', status=200, mimetype='application/json') 

    return Response('{"status": "success", "Found": "true", "discordId": '+json.loads(open(f"./VerifyQueue/{username}.txt").read())["discordId"]+', "tag": "'+json.loads(open(f"./VerifyQueue/{username}.txt").read())["tag"]+'"}', status=200, mimetype='application/json') 

@app.route('/api/v1/rank', methods=['POST'])
def api_rank():
    data = request.args 
    if len(data) < 1:
        data = json.loads(request.data)

    if not "key" in data or not "cookie" in data or not "username" or not "groupid" or not "rank":
        return Response('{"status": "invalid"}', status=400, mimetype='application/json')

    with open("./WebAPI/apiKeys.json", "r") as f:
        keys = json.loads(f.read())["used"]
        f.close()

    if not data["key"] in keys:
        return Response('{"status": "auth fail"}', status=403, mimetype='application/json')
    
    username = str(data["username"])
    cookie = str(data["cookie"])
    GroupId = data["groupid"]
    Rank = data["rank"]

    if isinstance(GroupId, str):
        if not GroupId.isnumeric():
            return Response('{"status": "please provide a number as groupid"}', status=406, mimetype='application/json')
        else:
            GroupId = int(GroupId)

    if isinstance(Rank, str):
        if not Rank.isnumeric():
            return Response('{"status": "please provide a number as rank"}', status=406, mimetype='application/json')
        else:
            Rank = int(Rank)

    GroupId = str(GroupId)

    userResponse = requests.get("http://api.roblox.com/users/get-by-username?username="+username)

    if userResponse.status_code == 200:
        userResponse = json.loads(userResponse.text)
        if not "Id" in userResponse:
            return Response('{"status": "User dosent exist"}', status=406, mimetype='application/json')
    else:
        return Response('{"status": "API error, try again later"}', status=503, mimetype='application/json')

    groupExist = groupexist(0, GroupId)

    if groupExist == "unavailable":
        return Response('{"status": "Invalid group ID or API error."}', status=406, mimetype='application/json')

    groupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(userResponse["Id"])+"/groups/roles?limit=100")

    if groupResponse.status_code == 200:
        Found = False
        UserIndex = 0
        groupResponse = json.loads(groupResponse.text)
        for i in groupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            UserIndex += 1

        if Found == False:
            return Response('{"status": "User not in group."}', status=406, mimetype='application/json')
    else:
        return Response('{"status": "API error, try again later"}', status=503, mimetype='application/json')

    verCookie = valCookie(cookie)

    if verCookie != 200:
        return Response('{"status": "Invalid cookie or api error."}', status=406, mimetype='application/json')

    x_csrf_token = get_x_csrf_token(cookie)

    if x_csrf_token:
        getBotUserSession = requests.get("https://www.roblox.com/my/profile", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})
        if getBotUserSession.status_code == 200:
            getBotUserSession = json.loads(getBotUserSession.text)
        else:
            return Response('{"status": "API error, try again later"}', status=503, mimetype='application/json')
    else:
        return Response('{"status": "Unable to grab X-CSRF-TOKEN"}', status=500, mimetype='application/json')

    botId = getBotUserSession["UserId"]
    botGroupResponse = requests.get("https://groups.roblox.com/v1/users/"+str(botId)+"/groups/roles?limit=100")

    if botGroupResponse.status_code == 200:
        Found = False
        Index = 0
        botGroupResponse = json.loads(botGroupResponse.text)
        for i in botGroupResponse["data"]:
            if i["group"]["name"] == groupExist["name"]:
                Found = True 
                break
            Index +=1

        if Found == False:
            return Response('{"status": "Bot not  in group"}', status=406, mimetype='application/json')
    else:
        return Response('{"status": "API error, try again later"}', status=503, mimetype='application/json')

    if groupResponse["data"][UserIndex]["role"]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
        return Response('{"status": "User role is higher than bot role."}', status=500, mimetype='application/json')

    rolesResponse = requests.get("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/roles", headers={"X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rolesResponse.status_code == 200:
        rolesResponse = json.loads(rolesResponse.text)
        RoleIndex = 0
        for i in rolesResponse["roles"]:
            if i["id"] == groupResponse["data"][UserIndex]["role"]["id"]:
                break
            RoleIndex += 1

        roleDesg = 0
        for i in rolesResponse["roles"]:
            if i["rank"] == int(Rank):
                break
            roleDesg += 1

        try:
            rolesResponse["roles"][roleDesg]
        except:
            return Response('{"status": "I was unable to find a roleset with your rankId."}', status=500, mimetype='application/json')

        if rolesResponse["roles"][roleDesg]["rank"] >= botGroupResponse["data"][Index]["role"]["rank"]:
            return Response('{"status": "Roleset is higher or same with bot role."}', status=500, mimetype='application/json')
    else:
        return Response('{"status": "API error, try again later"}', status=503, mimetype='application/json')

    rankRequest = requests.patch("https://groups.roblox.com/v1/groups/"+str(groupExist["id"])+"/users/"+str(userResponse["Id"]), data=json.dumps({
        "roleId": rolesResponse["roles"][roleDesg]["id"]
    }), headers={"content-type":"application/json","X-CSRF-TOKEN": x_csrf_token}, cookies={".ROBLOSECURITY": cookie})

    if rankRequest.status_code == 200:
        return Response('{"status": "success"}', status=200, mimetype='application/json')
    else:
        return Response('{"status": "Unable to change role."}', status=500, mimetype='application/json')

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)