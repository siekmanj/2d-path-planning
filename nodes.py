from segment import *
import math

#This is a base node class for the tangent implementation of djikstras algorithm

class NodeBase:
    def __init__(self,position,type):
        self.position = position
        self.pathDistance = 99999#Essentially infinity
        self.type = type#-1: Concave Vertex 0: point 1-n:obstacle number
        self.known = False
        self.parent = 0

class ObstacleNode(NodeBase):
    def __init__(self,obstacle,direction,type,ignoreSegs = None):
        super().__init__(obstacle.position,type)
        self.obstacle = obstacle
        self.radius = obstacle.radius
        self.direction = direction#1: CCW -1:CW
        self.firstAngle = 0#Angle from the previous intersection on the surface of the circle measure positively from the +x axis
        self.secondAngle = 0#Angle from the next intersection on the surface of the circle measure positively from the +x axis
        self.ignoreSegs = ignoreSegs
        self.segmentIn = Segment(self.position,self.position)

    def getCoTanSeg(self, obsnode):
        #Find the the cotangent line segment between the first and the second obstacle with given directions on both
        r1 = self.radius
        r2 = obsnode.radius

        length = self.position.distanceTo(obsnode.position)

        dy = obsnode.position.y - self.position.y
        dx = obsnode.position.x - self.position.x

        gamma = -1 * math.atan2(dy,dx)

        #Check if it is external or internal
        if self.direction == obsnode.direction:
            beta = math.asin((r2-r1)/length)
        else:
            beta = math.asin((r2+r1)/length)

        if self.direction == -1:
            startAngle = math.pi/2
            if obsnode.direction == -1:
                alpha = gamma - beta
            else:
                alpha = gamma + beta
        else:
            startAngle = 3*math.pi/2
            if obsnode.direction == -1:
                alpha = gamma - beta
            else:
                alpha = gamma + beta


        x3 = self.position.x + r1*math.cos(startAngle-alpha)
        y3 = self.position.y + r1*math.sin(startAngle-alpha)
        x4 = obsnode.position.x + self.direction*obsnode.direction*r2 * math.cos(startAngle - alpha)
        y4 = obsnode.position.y + self.direction*obsnode.direction*r2 * math.sin(startAngle - alpha)

        #Calculate the second angle for the cotangent line
        dy = y3-self.position.y
        dx = x3 - self.position.x
        self.secondAngle = math.atan2(dy,dx)





        startPos = Position(x3,y3)
        endPos = Position(x4,y4)

        #Create the cotangent segment
        coTanSegment = Segment(startPos,endPos)

        return coTanSegment

    def getArcDistance(self):
        if self.firstAngle < 0:
            self.firstAngle += 2*math.pi
        elif self.firstAngle > 2*math.pi:
            self.firstAngle -= 2*math.pi

        if self.secondAngle < 0:
            self.secondAngle += 2 * math.pi
        elif self.secondAngle > 2 * math.pi:
            self.secondAngle -= 2 * math.pi
        angle_diff = self.firstAngle - self.secondAngle

        #if self.direction == -1:
        #    angle_diff = 2*math.pi-angle_diff

        arcDistance  = self.radius*angle_diff
        #print(angle_diff)
        return abs(arcDistance)

    def getCircleIntersection(self,obstacles):
        # Normalize both of the angles to between 0 and 2pi
        if self.firstAngle < 0:
            self.firstAngle += 2*math.pi
        elif self.firstAngle > 2*math.pi:
            self.firstAngle -= 2*math.pi

        if self.secondAngle < 0:
            self.secondAngle += 2 * math.pi
        elif self.secondAngle > 2 * math.pi:
            self.secondAngle -= 2 * math.pi


        for obs in obstacles:
            dx = obs.position.x - self.obstacle.position.x
            dy = obs.position.y - self.obstacle.position.y
            obsAngle = math.atan2(dy,dx)
            if self.firstAngle < self.secondAngle:
                if self.direction == 1:
                    if obsAngle < self.secondAngle and obsAngle > self.firstAngle:
                        if self.obstacle.distanceTo(obs.position) < obs.radius:
                            return True
                else:
                    if obsAngle < self.firstAngle and obsAngle > self.secondAngle - math.pi*2:
                        if self.obstacle.distanceTo(obs.position) < obs.radius:
                            return True
            elif self.firstAngle > self.secondAngle:
                if self.direction == 1:
                    if obsAngle > self.firstAngle - math.pi*2 and obsAngle < self.secondAngle:
                        if self.obstacle.distanceTo(obs.position) < obs.radius:
                            return True
                else:
                    if obsAngle < self.firstAngle and obsAngle > self.secondAngle:
                        if self.obstacle.distanceTo(obs.position) < obs.radius:
                            return True

        #If none of the other conditions are met
        return False



    def getDistanceTo(self,obsnode,circleStart):
        # CircleStart: Boolean that represents whether or not it starts on a circle or just a node
        coTanSegment = self.getCoTanSeg(obsnode)

        distance = coTanSegment.getLength()

        if circleStart:
            distance += self.getArcDistance()

        return distance+self.pathDistance
