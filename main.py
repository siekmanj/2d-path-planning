#!/usr/bin/env python3
import load_files
import save_files
import config
import fieldgen
import gravity
import tanDjikstra

from drawObstaclesPath import drawObstaclesPath

waypoint_list, obstacle_list, bound_segments = fieldgen.fieldGen(config.FIELD_WIDTH,
                                                 config.FIELD_HEIGHT,
                                                 config.USE_GUI,
                                                 config.NUM_OBSTACLE,
                                                 config.NUM_WAYPOINTS,
                                                 config.NUM_BOUND_PTS)

paths = []  # append your paths to this list to draw them all at once (for comparison)
realpath, allpaths, workpath = tanDjikstra.tangentDjikstra(waypoint_list,obstacle_list,bound_segments)
paths.append(allpaths)
paths.append(workpath)
paths.append(realpath)

#paths.append(gravity.simplegravity(obstacle_list, waypoint_list, config.FIELD_HEIGHT, config.FIELD_WIDTH))


save_files.save_files(paths, waypoint_list, obstacle_list)
# load_files.load_files()

drawObstaclesPath(obstacle_list, paths, bound_segments, waypoint_list, config.FIELD_HEIGHT, config.FIELD_WIDTH)
