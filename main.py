import random
import math
from tkinter import *

class Obstacle:
    def __init__(self):
        #give an obstacle random x and y coordinates, and a random radius
        random.seed()
        
        self.radius = random.uniform(40, 50)
        self.x = random.uniform(0+self.radius, 1000-self.radius)
        self.y = random.uniform(0+self.radius, 500-self.radius)
        
    def distanceFromPoint(self, x, y):
        #returns the distance from a pair of xy coordinates to the object
        return math.sqrt(math.pow(self.x-x, 2) + math.pow(self.y-y, 2)) - self.radius

#initialize an empty list
obstacle_list = []

#add 11 obstacles to the list
for i in range(11):
    obstacle_list.append(Obstacle())

#visualization stuff
master = Tk()
w = Canvas(master, width=1000, height=600)
w.pack()

#draw the obstacles on the canvas
for i in obstacle_list:
    w.create_oval(i.x+i.radius, i.y+i.radius, i.x-i.radius, i.y-i.radius, fill="red")

mainloop()