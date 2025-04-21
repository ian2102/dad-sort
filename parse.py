import re
import scheme

NUMBERS_REGEX = r'-?\d+\.\d+|-?\d+'

def parse_text(og_text):
    # remove everything thats not a number or letter
    text = re.sub(r"[^a-zA-Z0-9 \n.-]", " ", og_text).lower()

    print(text)

    item = {
        "name": "0",
        "rarity": "Common",
    }

    # rarity
    escape = False
    lines = text.split("\n")
    for line in lines:
        if escape:
            break
        for rarity in scheme.raritys:
            if rarity.lower() in line:
                item["rarity"] = rarity
                escape = True
                break
    
    # name
    for line in lines:
        hits = []
        for name in scheme.names:
            if name.lower() in line:
                print("Name", name)
                hits.append(name)

        # if its FrostlightCrusaderHelm we dont want to go with CrusaderHelm
        if hits:
            print(hits)
            name = max(hits, key=len)
            item["name"] = name
    
    with open("output.txt", "a") as file:
        text = f"""
{og_text}
----------
Item:
{item['name']}, {item['rarity']}
"""
        file.write(text)

    return (item, og_text)

text = """Potion of Protection

Move Speed -10

Gain a shield that blocks 10 physical damage
for 24 seconds.

Slot Type: Utility

Utility Type: Drink

Loot State: Handled
Rarity: Poor

Potion that gives a temporary defensive
shield around the user."""

if __name__ == "__main__":
    print(scheme.raritys)
    print(scheme.names)
    item, og_text = parse_text(text)
    print(item)