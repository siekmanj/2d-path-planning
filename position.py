import math


# this class represents a position on an xy plane. It includes methods for calculating the distance to points and determining whether it is inside a rectangle
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanceTo(self, position):
        return math.sqrt(math.pow(self.x - position.x, 2) + math.pow(self.y - position.y, 2))

    def within(self, xlower, ylower, xhigher, yhigher):
        if self.x < xhigher and self.x > xlower and self.y < yhigher and self.y > ylower:
            return True
        return False

    def angle(self, pos):
        return math.atan2(self.y - pos.y, self.x - pos.x)

    def withinObstacles(self, obstacles):
        withinObst = False
        for obstacle in obstacles:
            if self.distanceTo(obstacle.position) < obstacle.radius:
                withinObst = True
        return withinObst

    def inBounds(self,boundSegments):
        #Use raycasting to figure out whether or not the point is within the obstacle
        num_intersections = 0;
        for boundSeg in boundSegments:
            num_intersections += boundSeg.rayIntersection(self)

        if num_intersections % 2 == 1:
            return True
        else:
            return False

    def viablePoint(self,boundSegments, obstacles):
        if self.inBounds(boundSegments) and not self.withinObstacles(obstacles):
            return True
        else:
            return False
