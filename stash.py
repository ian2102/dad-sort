import macros
import image
import parse
from item import Item
import heapq
from point import Point
import scheme

class Stash:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stash = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.pq = []

    def move(self, start_pos, end_pos):
        print(f"Moving: {start_pos} to {end_pos}")

        if start_pos == end_pos:
            print(f"start_pos == end_pos")
            return
        
        item = self.stash[start_pos.x][start_pos.y]
        if item == 0:
            print(f"No item at start_pos: {start_pos}")
            return
        else:
            print(f"Moving: {item}")
        
        # Check that new position is within bounds
        if (end_pos.x + item.width > self.width) or (end_pos.y + item.height > self.height):
            print(f"Error: Cannot move {item} to {end_pos} — out of bounds!")
            return

        # Clear old location
        for dx in range(item.width):
            for dy in range(item.height):
                self.stash[start_pos.x + dx][start_pos.y + dy] = 0

        # Place item in new location
        for dx in range(item.width):
            for dy in range(item.height):
                self.stash[end_pos.x + dx][end_pos.y + dy] = item

        macros.move_from_to(start_pos, end_pos)
        item.position = end_pos

    def intersects(item1, item2):
        x1, y1 = item1.position.x, item1.position.y
        w1, h1 = item1.width, item1.height

        x2, y2 = item2.position.x, item2.position.y
        w2, h2 = item2.width, item2.height

        return not (
            x1 + w1 <= x2 or
            x2 + w2 <= x1 or
            y1 + h1 <= y2 or
            y2 + h2 <= y1
        )
    
    def find_empty_slot(self, item):
        for y in range(self.height - item.height, -1, -1):
            for x in range(self.width - item.width, -1, -1):
                go_next = False
                for dx in range(item.width):
                    for dy in range(item.height):
                        if self.stash[x + dx][y + dy] != 0:
                            go_next = True
                            break
                    if go_next:
                        break
                if not go_next:
                    return Point(x, y)
                
    def hover_all_stash(self):
        to_check = []
        for x in range(self.width):
            for y in range(self.height):
                to_check.append(Point(x, y))
        
        while to_check:
            point = to_check.pop(0)
            macros.hover_stash(point)

            # If already filled, skip it
            if self.stash[point.x][point.y] != 0:
                continue

            screenshot = image.get_screenshot_np()
            tooltip = image.get_tooltip(screenshot)
            if tooltip is not None:
                text = image.image_to_text(tooltip)
                output = parse.parse_text(text)

                item = output[0]
                item = Item.from_dict(item)

                # unidentified item
                if item.name == "0":
                    item.width, item.height = 1, 1
                else:
                    item.width, item.height = scheme.get_dimensions(item.name)
                    item.position = point

                # Mark all stash cells the item occupies
                for dx in range(item.width):
                    for dy in range(item.height):
                        x, y = point.x + dx, point.y + dy
                        if 0 <= x < self.width and 0 <= y < self.height:
                            self.stash[x][y] = item
                            # Remove the used point, if it's still there
                            if Point(x, y) in to_check:
                                to_check.remove(Point(x, y))

                heapq.heappush(self.pq, item)

    def __repr__(self):
        grid = [["." for _ in range(self.width)] for _ in range(self.height)]

        for x in range(self.width):
            for y in range(self.height):
                item = self.stash[x][y]
                if item != 0:
                    # Just display the first letter of the item name or a hash of it
                    grid[y][x] = item.name[0].upper() if item.name else "#"

        # Create a string representation row by row
        lines = []
        for row in grid:
            lines.append(" ".join(row))
        return "\n".join(lines)
