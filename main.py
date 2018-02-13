import fanpath
import fieldgen
import rubberpath
from tkinter import *

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
NUM_WAYPOINTS = 2
NUM_OBSTACLE = 10
USE_GUI = False#Whether to enable the gui

#0:fanpath
#1:rubberpath
WHICH_ALGORITHM = 0

waypoint_list, obstacle_list = fieldgen.fieldGen(FIELD_WIDTH, FIELD_HEIGHT,USE_GUI , NUM_OBSTACLE, NUM_WAYPOINTS)

#visualization stuff
master = Tk()
w = Canvas(master, width=FIELD_WIDTH, height=FIELD_HEIGHT)
w.pack()

#draw the obstacles on the canvas
for i in obstacle_list:
    w.create_oval(i.position.x+i.radius, i.position.y+i.radius, i.position.x-i.radius, i.position.y-i.radius, fill="red")


if WHICH_ALGORITHM == 0:
    path = fanpath.simplefan(obstacle_list, waypoint_list[0], waypoint_list[1])

    lastx = waypoint_list[0].x
    lasty = waypoint_list[0].y
    for coord in path:
        w.create_line(lastx, lasty, coord.x, coord.y)
        lastx = coord.x
        lasty = coord.y
else:
    segmentspath = rubberpath.rubberpath(obstacle_list,waypoint_list)

    for segment in segmentspath:
        w.create_line(segment.startPos.x,segment.startPos.y,segment.endPos.x,segment.endPos.y)


mainloop()
