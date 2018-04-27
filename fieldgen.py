from obstacleCanvas import *
from boundingSegment import *
import random


def fieldGen(width, height, guiInput, numObstacles, numWaypoints, numBoundPts):
    '''
    def obstacleGen:
    This is a function that will create the obstacles that will be used for path planning and if user input is selected,
    will allow the user to choose the starting and the ending waypoints

    width: Width of the field in px
    height: Height of the field in px
    guiInput: Boolean of whether the user wants a gui input of the obstacles
    numObstacles: Number of obstacles(only for random generation)
    '''
    # initialize an empty list
    obstacle_list = []
    waypoint_list = []
    bound_segments= []
    bound_pts = []

    if guiInput:
        '''
        Initialize tkinter canvas
        get user input for waypoint start and end
        get user input for location and size of obstacles
        '''
        # Create tkinter canvas
        root = Tk()
        window = ObstacleCanvas(root, numWaypoints, numBoundPts, width=width, height=height)
        window.pack()

        def endgui(event):
            nonlocal root
            nonlocal obstacle_list
            nonlocal waypoint_list
            nonlocal bound_pts
            nonlocal window
            waypoint_list = window.waypoints
            obstacle_list = window.obstacles
            bound_pts = window.bound_pts
            root.destroy()

        root.bind("q", endgui)

        root.mainloop()



    else:
        waypoint_list = []
        waypoint_list.append(Position(0, 0))
        waypoint_list.append(Position(width, height))

        # add 11 obstacles to the list
        for i in range(numObstacles):
            radius = random.uniform(40, 50)
            pos = Position(random.uniform(0 + radius, width - radius), random.uniform(0 + radius, height - radius))
            obst = Obstacle(pos, radius)
            obst.xspd = random.uniform(-10, 10)
            obst.yspd = random.uniform(-10, 10)
            print("rand")
            obstacle_list.append(Obstacle(pos, radius))

    #Convert the bound_pts to bound_segments
    for i in range(len(bound_pts),0,-1):
        bound_segments.append(BoundSegment(bound_pts[i-1],bound_pts[i-2]))


    return waypoint_list, obstacle_list, bound_segments
