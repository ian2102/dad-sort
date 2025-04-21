import pyautogui
from point import Point

# all positions are for 1920x1080 resolution

inv = Point(705, 644)

stash = Point(1394, 218)
jump = 40

def hover_stash(point):
    pyautogui.moveTo(stash.x + (jump * point.x), stash.y + (jump * point.y))

def move_from_to(start_pos, end_pos):
    start_x = stash.x + (jump * start_pos.x)
    start_y = stash.y + (jump * start_pos.y) 
    end_x = stash.x + (jump * end_pos.x)
    end_y = stash.y + (jump * end_pos.y)

    pyautogui.moveTo(start_x, start_y, duration=0.1)
    pyautogui.mouseDown()
    pyautogui.moveTo(end_x, end_y, duration=0.2)
    pyautogui.mouseUp()