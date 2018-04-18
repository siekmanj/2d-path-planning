'This file will contain all of the mathematical functions used in path planning that are more general'
import math

def getAngleFromX(dx,dy):
    if dx == 0:
        if dy > 0:
            theta = math.pi
        else:
            theta = -1 * math.pi
    else:
        theta = math.atan2(dy,dx)

    return theta