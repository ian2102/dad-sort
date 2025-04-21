import re
import scheme

NUMBERS_REGEX = r'-?\d+\.\d+|-?\d+'

def parse_text(og_text):
    # remove everything thats not a number or letter
    text = re.sub(r"[^a-zA-Z0-9 \n.-]", " ", og_text).lower()

    item = {
        "name": "0",
        "rarity": "Common",
        "pp": [],
        "sp": []
    }

    # indexs of lines we want to remove
    indexs = []

    # rarity
    escape = False
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if escape:
            break
        for rarity in scheme.raritys:
            if rarity.lower() in line:
                item["rarity"] = rarity
                indexs.extend(range(index + 1, len(lines)))
                escape = True
                break
    
    # name
    for index, line in enumerate(lines):
        hits = []
        for name in scheme.names:
            if name.lower() in line:
                hits.append(name)

        # if its FrostlightCrusaderHelm we dont want to go with CrusaderHelm
        if hits:
            name = max(hits, key=len)
            item["name"] = name
            indexs.append(index)
    
    with open("output.txt", "a") as file:
        text = f"""
{og_text}
----------
Item:
{item['name']}, {item['rarity']}
"""
        file.write(text)

    return (item, og_text)