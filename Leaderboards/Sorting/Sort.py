
import time 
import json 
import os

def run():
    while True:
        total = 0
        with open("./Leaderboards/Sorting/Votes.json", "r") as file:
            data = json.loads(file.read())["votes"]
            file.close() 
        for i in range(len(data)):
            cursor = data[i]
            total += cursor["votes"]
            pos = i
        
            while pos > 0 and data[pos - 1]["votes"] < cursor["votes"]:
                data[pos] = data[pos - 1]
                pos = pos - 1

            data[pos] = cursor

        with open("./Leaderboards/Votes.json", "w") as file:
            data = file.write(json.dumps({
                "votes": data,
                "total": total
            }))
            file.close() 

        time.sleep(10)