#!/usr/bin/env python3
import drawObstaclesPath
import readFile

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600

PathFileName = 'paths'
WaypointFileName = 'waypoints'
ObstacleFileName = 'obstacles'

paths = readFile.readFile(PathFileName)
waypoint_list = readFile.readFile(WaypointFileName)
obstacle_list = readFile.readFile(ObstacleFileName)

drawObstaclesPath.drawObstaclesPath(obstacle_list,paths,FIELD_HEIGHT,FIELD_WIDTH)
