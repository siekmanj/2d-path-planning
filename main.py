import fanpath
import fieldgen
from tkinter import *

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
NUM_WAYPOINTS = 2
NUM_OBSTACLE = 10
USE_GUI = False#Whether to enable the gui

waypoint_list, obstacle_list = fieldgen.fieldGen(FIELD_WIDTH, FIELD_HEIGHT,USE_GUI , NUM_OBSTACLE, NUM_WAYPOINTS)

#visualization stuff
master = Tk()
w = Canvas(master, width=FIELD_WIDTH, height=FIELD_HEIGHT)
w.pack()

#draw the obstacles on the canvas
for i in obstacle_list:
    w.create_oval(i.position.x+i.radius, i.position.y+i.radius, i.position.x-i.radius, i.position.y-i.radius, fill="red")

path1 = fanpath.simplefan(obstacle_list, waypoint_list[0], waypoint_list[1])
path2 = fanpath.simplefan(obstacle_list, waypoint_list[1], waypoint_list[0])

print(waypoint_list[0].x)
print(waypoint_list[0].y)
lastx = waypoint_list[0].x
lasty = waypoint_list[0].y
for coord in path1:
	w.create_line(lastx, lasty, coord.x, coord.y)
	lastx = coord.x
	lasty = coord.y
	
for coord in path2:
	w.create_line(lastx, lasty, coord.x, coord.y)
	lastx = coord.x
	lasty = coord.y
for coord in path1:
	for intersection in path2:
		if coord.x == intersection.x and coord.y == intersection.y:
			print("COLLISION AT: " + str(coord.x) + ", " + str(coord.y))
		
	

mainloop()
