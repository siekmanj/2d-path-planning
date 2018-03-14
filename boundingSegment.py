'''
This is a class that will be used for the boundaries of the flight zone.
'''

class BoundSegment:
    def __init__(self,startPos,endPos):
        self.startPos = startPos
        self.endPos = endPos

    def rayIntersection(self,pt):
        '''
        This method will check whether or not a ray horizontally from the left to the point intersects the segment
        It will then be used for the ray-casting algorithm to figure out whether or not the point is within the polygon.
        :param pt: instance of position for the point to check
        :return: true or false whether not the ray intersects the segment
        '''

        if self.startPos.y == self.endPos.y:
            return 0
        else:
            # A is the lower of the two points in y
            if self.startPos.y < self.endPos.y:
                A = self.startPos
                B = self.endPos
            else:
                A = self.endPos
                B = self.startPos

            #Check whether the point is outside the y range
            if pt.y <= A.y or pt.y >= B.y:
                return 0
            else:
                #Check whether the point is outside the x range
                if (pt.x < A.x and pt.x < B.x):
                    return 0
                elif (pt.x > A.x and pt.x > B.x):
                    return 1
                else:
                    #Set the slopes(dx/dy)
                    mPt = (pt.x-A.x)/(pt.y-A.y)#Slope from A to pt
                    mSeg = (B.x-A.x)/(B.y-A.y)#Slope of the segment
                    #Check to see if the slope of the point is greate
                    if mPt > mSeg:
                        return 1
                    else:
                        return 0