import position

class Obstacle:
    def __init__(self, pos, radius):
        self.radius = radius
        self.position = pos
        self.xspd = 0
        self.yspd = 0

    #returns the distance from a position object to the obstacle's position object
    def distanceTo(self, pos):
        return self.position.distanceTo(pos) - self.radius

    def step(self):
        self.position.x += self.xspd
        self.position.y += self.yspd
