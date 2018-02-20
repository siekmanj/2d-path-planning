'''
The goal of this program is to calculate a path for the uav to fly between two given waypoints by using the rubber band method talked about

Overview of the rubber band method:
Check for intersections between the path and the obstacles
for first intersection found, find the point closest to the center of the obstacle on path then move that point a buffer amount past edge
repeat until there are not any intersections left

****Lots of optimization is going to be needed here
while intersections
    intersections = false
    for each segment(1 less segment than number of points in path)
        segment1,segment2 = stretch
        if segment2 = 0
            continue
        else
            intersections = true
            segments[current] = segment1
            segments.insert(current+1,segment2)
'''
from segment import *
import drawObstaclesPath

def rubberpath(obstacle_list,waypoint_list,draw,height,width):
    overall_path = []

    #segments holds the path from one waypoint to another
    segments = []
    #Add the initial segments to the path
    for i in range(len(waypoint_list)-1):
        segments.append(Segment(waypoint_list[i],waypoint_list[i+1]))



    intersections = True
    while intersections:
        #reset intersections to false and only set to true of one is found
        intersections = False
        numintersections = 0
        numSegments = len(segments)
        buffer_segments = []
        for j in range(0,numSegments):
            segment1,segment2 = segments[j].stretch(obstacle_list,5)
            buffer_segments.append(segment1)
            if segment2 != 0:
                intersections = True
                buffer_segments.append(segment2)
                numintersections += 1
            if draw:
                # prep the paths variable for drawing
                paths = [segments,buffer_segments]
                drawObstaclesPath.drawObstaclesPath(obstacle_list, paths, height, width)

        segments = buffer_segments






    return segments