import random
import json

data = {"Steps": [],
        "Calories":[], 
        "Heart Rate":[],
        "Respiratory Rate":[], #BRPM (breaths per minute)
        "Hours Slept":[],
        "Body Temperature":[],
        "Blood Pressure":[]
        }
for i in range(10):
    data["Steps"].append(random.randint(0, 150))
    data["Calories"].append(random.randint(00, 300))
    data["Hours Slept"].append(random.randint(3, 12))
for i in range(10):   
    data["Heart Rate"].append(random.randint(60, 120))
    data["Respiratory Rate"].append(random.randint(10, 30))
    data["Body Temperature"].append(round(random.uniform(35.0, 40.0), 1))
    data["Blood Pressure"].append(random.randint(70, 130))
   
with open("smartwatchrandom_data.json", "w") as outfile:
    json.dump(data, outfile)

