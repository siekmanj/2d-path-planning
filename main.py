#!/usr/bin/env python3
import load_files
import save_files
import config
import fieldgen
import tanDjikstra
import pathToPoints
import ProfilePath
import numpy as np
from drawObstaclesPath import drawObstaclesPath

waypoint_list, obstacle_list, bound_segments = fieldgen.fieldGen(config.FIELD_WIDTH,
                                                 config.FIELD_HEIGHT,
                                                 config.USE_GUI,
                                                 config.NUM_OBSTACLE,
                                                 config.NUM_WAYPOINTS,
                                                 config.NUM_BOUND_PTS)

#*****I don't know how to put this in the config file, but should figure it out. Temporarily defined here
fc = {"thrust":50,
      "mass":4,
      "density":1.225,
      "cd":1,
      "refarea":.25,
      "veff": 14}#Flight characteristics of the drone

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
drawObstaclesPath(obstacle_list, paths, bound_segments, waypoint_list, config.FIELD_HEIGHT, config.FIELD_WIDTH)

#-----------Motion Profiling Section--------------
pathWaypoints = pathToPoints.pathToPoints(realpath)#Convert to simply the points

#Eventually the powercurve will need to be some experimetnally obtained data
pvf = np.linspace(0,100,100)

powercurve = np.tile(pvf, (len(pvf),1))

_,times,vprofile,points = ProfilePath.ProfilePath(pathWaypoints,fc,config.NUM_SPLINE_PTS,powercurve)


