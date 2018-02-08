import random
import math
import fanpath
from position import *
from obstacle import *
from tkinter import *

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600


#initialize an empty list
obstacle_list = []

#add 11 obstacles to the list
for i in range(11):
    radius = random.uniform(40, 50)
    pos = Position(random.uniform(0+radius, FIELD_WIDTH-radius), random.uniform(0+radius, FIELD_HEIGHT-radius))
    obstacle_list.append(Obstacle(pos, radius))

#visualization stuff
master = Tk()
w = Canvas(master, width=FIELD_WIDTH, height=FIELD_HEIGHT)
w.pack()

#draw the obstacles on the canvas
for i in obstacle_list:
    w.create_oval(i.position.x+i.radius, i.position.y+i.radius, i.position.x-i.radius, i.position.y-i.radius, fill="red")

startpos = Position(0, 0)
endpos = Position(FIELD_WIDTH, FIELD_HEIGHT)

path = fanpath.calculatepath(obstacle_list, startpos, endpos)

lastx = 0
lasty = 0
for coord in path:
    w.create_line(lastx, lasty, coord.x, coord.y)
    lastx = coord.x
    lasty = coord.y


mainloop()