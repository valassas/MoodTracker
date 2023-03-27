import random
import json

data = {"Steps": [],
        "Calories":[],
        "Heart Rate":[],
        "FUCK":[]
        }
for i in range(4):
    data["Steps"].append(random.randint(0, 150))
    data["Calories"].append(random.randint(00, 300))
    data["Heart Rate"].append(random.randint(3, 12))
    data["FUCK"].append(random.randint(3, 12))


with open("smartwatchrandom_data.json", "w") as outfile:
    json.dump(data, outfile)