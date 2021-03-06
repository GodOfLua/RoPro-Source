import flask
from flask import request, jsonify
from flask import Response
import os,sys
import json 

app = flask.Flask(__name__)
app.config["DEBUG"] = True

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

app.run('0.0.0.0', debug=True, port=5000)