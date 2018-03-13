from tkinter import *
from obstacleCanvas import *
import random

def fieldGen(width,height,guiInput,numObstacles,numWaypoints):
    '''
    def obstacleGen:
    This is a function that will create the obstacles that will be used for path planning and if user input is selected,
    will allow the user to choose the starting and the ending waypoints
    
    width: Width of the field in px
    height: Height of the field in px
    guiInput: Boolean of whether the user wants a gui input of the obstacles
    numObstacles: Number of obstacles(only for random generation) 
    '''
    #initialize an empty list
    obstacle_list = []
    waypoint_list = []

    if guiInput:
        '''
        Initialize tkinter canvas
        get user input for waypoint start and end
        get user input for location and size of obstacles
        '''
        #Create tkinter canvas
        root = Tk()
        window = ObstacleCanvas(root,numWaypoints, width=width, height=height)
        window.pack()

        def endgui(event):
            nonlocal root
            nonlocal obstacle_list
            nonlocal waypoint_list
            nonlocal window
            waypoint_list = window.waypoints
            obstacle_list = window.obstacles
            root.destroy()

        root.bind("q",endgui)



        root.mainloop()



    else:
        waypoint_list = []
        waypoint_list.append(Position(0, 0))
        waypoint_list.append(Position(width, height))

        #add 11 obstacles to the list
        for i in range(numObstacles):
            radius = random.uniform(40, 50)
            pos = Position(random.uniform(0+radius, width-radius), random.uniform(0+radius, height-radius))
            obstacle_list.append(Obstacle(pos, radius))

    return waypoint_list,obstacle_list