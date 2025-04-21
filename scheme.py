import os
import json

ITEMS_PATH = 'Items'

raritys = ["Junk", "Poor", "Common", "Uncommon", "Rare", "Epic", "Legendary", "Unique"]
names = [
    os.path.splitext(f)[0] 
    for f in os.listdir(ITEMS_PATH) 
    if os.path.isfile(os.path.join(ITEMS_PATH, f))
]

def get_dimensions(name):
    path = os.path.join(ITEMS_PATH, name + ".json")
    with open(path, "r") as file:
        data = json.load(file)
    return data.get("invwidth"), data.get("invheight")
