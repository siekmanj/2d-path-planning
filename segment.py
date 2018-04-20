from position import *

class Segment:
    def __init__(self,startPos,endPos):
        self.startPos = startPos
        self.endPos = endPos

    def getLength(self):
        return self.startPos.distanceTo(self.endPos)

    def minDistancePoint(self,point):
        #Function to find the point along a line that is closest to another point
        #If that point does no lie in between the start and the end points of the segment it will return 0
        minDistancePt = Position(0,0)
        #Eliminate cases where the slope or its reciprocal divides by 0
        if self.startPos.x == self.endPos.x:
            #Distance is simply the horizontal distance
            minDistancePt.x = self.startPos.x
            minDistancePt.y = point.y
        elif self.startPos.y == self.endPos.y:
            #Distance is simply the vertical distance
            minDistancePt.y = self.startPos.y
            minDistancePt.x = point.x
        else:
            #Must be somewhere in between
            #Solve system of equations
            #y=mx+b
            #b = y0-mx0
            #y1 = (-1/m)x1+b1d
            #b1 = y1-x1(-1/m)
            #mx + y0 - mx0 = (-1/m)x+y1-x1(-1/m)
            #mx+(1/m)x=mx0-y0+y1+x1(1/m)
            #xf = (mx0-y0+y1+x1(1/m))/(m+1/m)
            #yf = mxf + y0 - mx0
            m = (self.endPos.y-self.startPos.y)/(self.endPos.x-self.startPos.x)
            minDistancePt.x = (m*self.startPos.x-self.startPos.y+point.y+point.x*(1/m))/(m+1/m)
            minDistancePt.y = m*minDistancePt.x+self.startPos.y-m*self.startPos.x


        #Check if it is outside of the line segment
        if(minDistancePt.x < self.startPos.x and minDistancePt.x < self.endPos.x)and(minDistancePt.y < self.startPos.y and minDistancePt.y < self.endPos.y)\
                or(minDistancePt.x > self.startPos.x and minDistancePt.x > self.endPos.x)and(minDistancePt.y > self.startPos.y and minDistancePt.y > self.endPos.y) \
                or (minDistancePt.x > self.startPos.x and minDistancePt.x > self.endPos.x) and (minDistancePt.y < self.startPos.y and minDistancePt.y < self.endPos.y) \
                or (minDistancePt.x < self.startPos.x and minDistancePt.x < self.endPos.x) and (minDistancePt.y > self.startPos.y and minDistancePt.y > self.endPos.y):
            return 0
        else:
            return minDistancePt

    def closestIntersection(self,obstacles):
        #This function searches through all of a list of obstacle classes, sorting them by how close they are to the startpos
        #Then it find the first one with which there is a collision and returns the closes point along the segment
        #as well as the obstacle of interest
        returned = False
        obstacle_list = obstacles
        obstacle_list.sort(key=lambda obst: obst.distanceTo(self.startPos))
        for obstacle in obstacles:
            minDistancePt = self.minDistancePoint(obstacle.position)
            if minDistancePt != 0:
                if minDistancePt.distanceTo(obstacle.position) < obstacle.radius+3:

                    return minDistancePt,obstacle
                    returned = True
                    break
        if not returned:
            return 0,0

    def getIntersectingObs(self,obstacles):
        # This function will iterate through all of the obstacles that are passed and will then find if there are any intersections with the obstacles, and if there are, it will return them
        for obs in obstacles:
            minDistancePt = self.minDistancePoint(obs.position)
            if minDistancePt != 0:
                if minDistancePt.distanceTo(obs.position) < obs.radius:
                    return True
        return False

    def getIntersectingSegs(self,allsegments,ignoreSegs = None):
        segments = allsegments[:]
        print('length segments')
        print(len(segments))
        if ignoreSegs != None:
            del segments[ignoreSegs[0]]
            del segments[ignoreSegs[1]]
        for seg in segments:
            # Check where the two lines would intersect
            x1i = self.startPos.x
            y1i = self.startPos.y
            x1f = self.endPos.x
            y1f = self.endPos.y

            x2i = seg.startPos.x
            y2i = seg.startPos.y
            x2f = seg.endPos.x
            y2f = seg.endPos.y

            # Calculate the change in x and the change in y for both
            dx1 = x1f - x1i
            dy1 = y1f - y1i

            dx2 = x2f - x2i
            dy2 = y2f - y2i
            #If both of the lines are paralell and vertical
            if dx1 == 0 and dx2 == 0:
                if x1i != x2i:
                    pass
                elif min(y2i, y2f) < y1i < max(y2i, y2f) or \
                        min(y2i, y2f) < y1f < max(y2i, y2f) or \
                        min(y1i, y1f) < y2i < max(y1i, y1f) or \
                        min(y1i, y1f) < y2f < max(y1i, y1f):
                    return True

            else:
                #***** Need to add another condition if either of the dx's are 0 or if the slopes are the same
                if dx1 == 0:
                    #Can't calculate the slope of 1, but can calculate the slope of 2
                    m2 = dy2 / dx2
                    #By definition if the first line is vertical the x value must be the same
                    xint = x1i
                    yint = m2*(xint-x2i)+y2i
                elif dx2 == 0:
                    #Can't calculate the slope of 2, but can calculate the slope of 1
                    m1 = dy1 / dx1
                    #By definition the x value must be that of the second line
                    xint = x2i
                    yint = m1*(xint-x1i)+y1i
                elif dy1/dx1 == dy2/dx2:
                    #If the slopes are the same, for our purposes we can say that they do not intersect
                    return False
                else:
                    m1 = dy1 / dx1
                    m2 = dy2 / dx2

                    xint = (m1 * x1i - y1i - m2 * x2i + y2i) / (m1 - m2)  # X value of the intersection of lines
                    yint = m1 * (xint - x1i) + y1i

                #Check whether or not the intersection point lies on both of the lines

                #Check if the point lies on both of the lines
                if min(x1i,x1f) < xint < max(x1i,x1f) and \
                        min(x2i, x2f) < xint < max(x2i, x2f) and \
                        min(y1i, y1f) < yint < max(y1i, y1f) and \
                        min(y2i, y2f) < yint < max(y2i, y2f):
                    return True
        return False

    def getIntersecting(self,obstacles,segments,ignoreSegs = None):
        if self.getIntersectingObs(obstacles):
            print('obstacle')
        if self.getIntersectingSegs(segments):
            print('segment')
        return self.getIntersectingObs(obstacles) or self.getIntersectingSegs(segments,ignoreSegs)

