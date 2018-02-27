#!/usr/bin/env python3
import fieldgen
import fanpath
import rubberpath
import drawObstaclesPath
import json
import pickle

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
NUM_WAYPOINTS = 2
NUM_OBSTACLE = 10
SHOW_RUBBER_STEPS = False
USE_GUI = False #Whether to enable the gui


waypoint_list, obstacle_list = fieldgen.fieldGen(FIELD_WIDTH, FIELD_HEIGHT,USE_GUI , NUM_OBSTACLE, NUM_WAYPOINTS)

paths = []  # append your paths to this list to draw them all at once (for comparison)
#paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'simplefan'))
paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'extendingfan'))
paths.append(rubberpath.rubberpath(obstacle_list, waypoint_list,SHOW_RUBBER_STEPS,FIELD_HEIGHT,FIELD_WIDTH))

print(paths)

for p in range(len(paths)):
  for i in range(len(paths[p])):
    print('path {} segment {}: sx={}, sy={};\tex={}, ey={}'.format(p, i, paths[p][i].startPos.x, paths[p][i].startPos.y, paths[p][i].endPos.x, paths[p][i].endPos.y))

outputFileName = 'paths.path'

print('Opening path output file {}'.format(outputFileName))
outputFile = open(outputFileName, 'wb')

pickle.dump(paths, outputFile)

outputFile.close()

inputFile = open(outputFileName, 'rb')
paths2 = pickle.load(inputFile)
inputFile.close()



#print(paths[1][0].startPos)

#for i in range(len(paths)):
#  print(paths[i].startPos)
#  print(paths[i].endPos)

drawObstaclesPath.drawObstaclesPath(obstacle_list,paths2,FIELD_HEIGHT,FIELD_WIDTH)
