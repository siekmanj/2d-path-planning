from tkinter import *
from position import *
from obstacle import *

class ObstacleCanvas(Canvas):
    def __init__(self,root, numWaypoints, width, height):
        Canvas.__init__(self, root, width=width, height=height)

        self.root = root

        #List of all of the obstacles that will be placed/waypoints
        self.obstacles = []#Instances of Obstacle
        self.waypoints = []#Instances of Position

        #Tkinter Object Lists
        self.obstacleCirles = []
        self.waypointCircles = [Position(0,0)]

        self.numWaypoints = numWaypoints

        self.defaultRad = 5#Default radius for waypoints and picking obstacle centers

        self.mousePos = Position(0,0)#Default initialization

        #Bind actions to events
        self.bind("<Button-1>",self.onClick)
        self.bind("<Motion>",self.onMotion)


    def setMousePos(self,event):
        #Bound to mouse movement in tkinter and updates position of the mouse
        self.mousePos.x = event.x
        self.mousePos.y = event.y


    def circleBounding(self,center,rad):
        #center: should be a instance of the Position class
        #rad: just a number
        #return the corner coords of a bounding rectangle around a circle give the center and the radius
        x0 = center.x - rad
        y0 = center.y - rad
        x1 = center.x + rad
        y1 = center.y + rad
        return x0,y0,x1,y1

    def onClick(self,event):
        self.setMousePos(event)
        if(len(self.waypoints) < self.numWaypoints):
            #Still in the placing waypoints phase

            #set the next waypoint to the position of the mouse
            self.waypoints.append(Position(self.mousePos.x,self.mousePos.y))
            x0, y0, x1, y1 = self.circleBounding(self.mousePos, self.defaultRad)
            self.waypointCircles[-1] = self.create_oval(x0, y0, x1, y1, outline='blue', width=2)
        else:
            #In the obstacle placing phase
            if(len(self.obstacles) == len(self.obstacleCirles)):
                #Placing radius of the obstacle
                self.obstacles[-1].radius = self.mousePos.distanceTo(self.obstacles[-1].position)
                #create the next circle in the drawing list

                #define the corners of the ellipse bounding box
                x0,y0,x1,y1 = self.circleBounding(self.mousePos,self.defaultRad)
                self.obstacleCirles.append(self.create_oval(x0,y0,x1,y1,outline='orange',width=2))
            else:
                #Placing center of the obstacle
                self.obstacles.append(Obstacle(Position(self.mousePos.x,self.mousePos.y),0))



    def onMotion(self,event):
        self.setMousePos(event)
        if(len(self.waypoints) < self.numWaypoints):
            #In the placing waypoints phase
            x0, y0, x1, y1 = self.circleBounding(self.mousePos, self.defaultRad)
            self.delete(self.waypointCircles[-1])
            self.waypointCircles[-1] = self.create_oval(x0, y0, x1, y1, outline='blue', width=2)

        else:
            #Check if the obstacle circles array is empty
            if(len(self.obstacleCirles) == 0):
                self.obstacleCirles.append(self.create_oval(0,0,1,1))

            #Now it must be an obstacle
            if (len(self.obstacles) == len(self.obstacleCirles)):
                #Placing the radius of the circle
                tempRad = self.mousePos.distanceTo(self.obstacles[-1].position)#Distance from the mouse the the center of the current object

                x0, y0, x1, y1 = self.circleBounding(self.obstacles[-1].position, tempRad)
                self.delete(self.obstacleCirles[-1])
                self.obstacleCirles[-1] = self.create_oval(x0,y0,x1,y1,outline='green',width=2)
            else:
                x0, y0, x1, y1 = self.circleBounding(self.mousePos, self.defaultRad)
                self.delete(self.obstacleCirles[-1])
                self.obstacleCirles[-1] = self.create_oval(x0, y0, x1, y1, outline='orange', width=2)





