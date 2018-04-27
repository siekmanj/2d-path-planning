import numpy as np

#This file will take the path that is calculated with the path planning algorithm and will then convert it to simply a numpy array of points


def pathToPoints(path):
    pathWaypoints = np.ones((2,len(path)))
    #Set the first point to the start of the first segment

    pathWaypoints[0, 0:-1] = path[0:-1].startPos.x
    pathWaypoints[1, 0:-1] = path[0:-1].startPos.y
    pathWaypoints[0, -1] = path[-1].endPos.x
    pathWaypoints[1, -1] = path[-1].endPos.y

    return pathWaypoints