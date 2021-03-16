
import time 
import json 
import os
from pathlib import Path

def run():
    while True:
        pathlist = Path("./Caching/Votes").rglob('*.json')
        for path in pathlist:
            with open(str(path), "r") as file:
                x = file.read()
                data = json.loads(x)
                file.close()
                with open("./Leaderboards/Sorting/Votes.json", "r") as file:
                    data2 = json.loads(file.read())
                    file.close()
                
                try:
                    data2["votes"][len(data2["votes"])-1]["id"]
                except:
                    data2["votes"].append({
                        "id": data["id"],
                        "votes": 0,
                        "name": data["name"]
                    })

                if data2["votes"][len(data2["votes"])-1]["id"] != data["id"]:
                    data2["votes"].append({
                        "id": data["id"],
                        "votes": 0,
                        "name": data["name"]
                    })
                data2["votes"][len(data2["votes"])-1]["votes"] += data["votes"]
                with open("./Leaderboards/Sorting/Votes.json", "w") as file:
                    file.write(json.dumps(data2))
                    file.close()
                os.remove(str(path))

        time.sleep(10)