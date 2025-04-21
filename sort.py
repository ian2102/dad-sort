import time
from stash import Stash
import heapq
from point import Point

def sort(stash):
    cur_x = 0
    cur_y = 0
    cur_height = 0
    while stash.pq:
        item = heapq.heappop(stash.pq)
        print("1. ", item)

        # check bounds and start a new row
        if cur_x + item.width > stash.width:
            cur_y += cur_height
            cur_height = item.height
            cur_x = 0
        
        if cur_y + item.height > stash.height:
            print("Out of space")
            return

        # clear space
        for x in range(item.width):
            for y in range(item.height):
                occupying_item = stash.stash[cur_x + x][cur_y + y]
                if occupying_item != 0 and occupying_item != item:
                    new_pos = stash.find_empty_slot(occupying_item)
                    if new_pos:
                        stash.move(occupying_item.position, new_pos)
                    else:
                        print("Cannot find valid temp location")

        stash.move(item.position, Point(cur_x, cur_y))
        cur_x += item.width

def main():
    time.sleep(2)

    # Stash Tab Default
    # WIDTH = 12
    # HEIGHT = 20
    WIDTH = 12
    HEIGHT = 20
    stash = Stash(WIDTH, HEIGHT)
    stash.hover_all_stash()
    print(stash)
    exit()
    sort(stash)

if __name__ == "__main__":
    main()
