from point import Point

class Item:
    def __init__(self, name, rarity, pp, sp, width, height):
        self.name = name
        self.rarity = rarity
        self.pp = pp
        self.sp = sp
        self.width = width
        self.height = height
        self.position = Point(0, 0)

    def __lt__(self, other):
        if self.height != other.height:
            return self.height > other.height
        if self.width != other.width:
            return self.width > other.width
        if self.rarity != other.rarity:
            return self.rarity > other.rarity
        return self.name < other.name
    
    def __eq__(self, other):
        if self and other:
            return self.name == other.name and self.rarity == other.rarity and self.position == other.position
    
    def __hash__(self):
        return hash((self.name, self.rarity, tuple(self.pp), tuple(self.sp)))

    def __repr__(self):
        return f"{self.rarity} {self.name} {self.width}X{self.height}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "rarity": self.rarity,
            "pp": self.pp,
            "sp": self.sp,
            "width": self.width,
            "height": self.height,
        }

    @staticmethod
    def from_dict(data):
        name = data.get("name", "Unnamed")
        rarity = data.get("rarity", "Common")
        pp = data.get("pp", [])
        sp = data.get("sp", [])
        return Item(name, rarity, pp, sp, 0, 0)
