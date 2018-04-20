from position import *
from segment import *
import math
import numpy as np
import customMath

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

        gamma = -1 * customMath.getAngleFromX(dx, dy)

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
        self.secondAngle = customMath.getAngleFromX(dx,dy)



        '''print('r1 = %d' % r1)
        print('r2 = %d' % r2)

        a = r1+r2
        print('a = %d' % a)

        length = self.position.distanceTo(obsnode.position)
        print('length = %d' % length)

        theta1 = math.asin(a/length)
        print('theta1 = %.3f' % theta1)

        dy = obsnode.position.y - self.position.y
        dx = obsnode.position.x - self.position.x

        print('dy = %d' % dy)
        print('dx = %d' % dx)

        #angle based on dy and dx
        theta2 = customMath.getAngleFromX(dx,dy)
        print('theta2 = %.4f' % theta2)

        theta3 = theta2 - theta1
        print('theta3 = %.4f' % theta3)
        self.secondAngle = math.pi / 2 * -1 * self.direction + theta3
        print('secondAngle = %.4f' % self.secondAngle)

        #create arrays for the ends of the tangent segment
        flat = np.array([[0,length],[-r1,-r1]])
        print(flat)
        c = math.cos(theta3)
        s = math.sin(theta3)
        rotation = np.array([[c,-s],[s,c]])

        translate = np.array([self.position.x,self.position.y])

        coTanSegEnds = np.transpose(np.transpose(rotation@flat) + translate)
        print(coTanSegEnds)
        '''


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
            obsAngle = customMath.getAngleFromX(dx,dy)
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
