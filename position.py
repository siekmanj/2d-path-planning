import math


# this class represents a position on an xy plane. It includes methods for calculating the distance to points and determining whether it is inside a rectangle
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, position):
        return math.sqrt(math.pow(self.x - position.x, 2) + math.pow(self.y - position.y, 2))

    def inBounds(self,boundSegments):
        #Use raycasting to figure out whether or not the point is within the obstacle
        num_intersections = 0;
        for boundSeg in boundSegments:
            num_intersections += boundSeg.rayIntersection(self)

        if num_intersections % 2 == 1:
            return True
        else:
            return False
