#!/usr/bin/env python3
import load_files
import save_files
import config
import fieldgen
import tanDjikstra
import planPath
import numpy as np

from drawObstaclesPath import drawObstaclesPath

waypoint_list, obstacle_list, bound_segments = fieldgen.fieldGen(config.FIELD_WIDTH,
                                                 config.FIELD_HEIGHT,
                                                 config.USE_GUI,
                                                 config.NUM_OBSTACLE,
                                                 config.NUM_WAYPOINTS,
                                                 config.NUM_BOUND_PTS,
                                                 config.FILENAME_MAPIMAGE)

#*****I don't know how to put this in the config file, but should figure it out. Temporarily defined here
fc = {"thrust":100,
      "mass":4,
      "density":1.225,
      "cd":1,
      "refarea":.25,
      "veff": 14}#Flight characteristics of the drone

# STATIC OBSTACLE PRINTING
paths = []  # append your paths to this list to draw them all at once (for comparison)
realpath, allpaths, nonintersectingpath = tanDjikstra.tangentDjikstra(waypoint_list,obstacle_list,bound_segments)
#paths.append(allpaths)
#paths.append(nonintersectingpath)
paths.append(realpath)
#paths.append(retiredalgorithms.rubberpath.rubberpath(obstacle_list,waypoint_list,False,config.FIELD_HEIGHT,config.FIELD_WIDTH))
#paths.append(retiredalgorithms.fanpath.simplefan(obstacle_list,waypoint_list[0],waypoint_list[1],config.FIELD_WIDTH,config.FIELD_HEIGHT))
#paths.append(gravity.simplegravity(obstacle_list, waypoint_list, config.FIELD_HEIGHT, config.FIELD_WIDTH))


save_files.save_files(paths, waypoint_list, obstacle_list)
# load_files.load_files()
drawObstaclesPath(obstacle_list, paths, bound_segments, waypoint_list, config.FIELD_HEIGHT, config.FIELD_WIDTH,config.FILENAME_MAPIMAGE)

# ANIMATION/MOVING OBSTACLE PRINTING

posTimes = planPath.planPath('tandji',obstacle_list,waypoint_list[1:],bound_segments,waypoint_list[0],fc,config)

#Save the positions and the times to a csv file
np.savetxt('AerialPath.csv',posTimes,delimiter=',')

