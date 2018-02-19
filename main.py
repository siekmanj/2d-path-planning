import fieldgen
import rubberpath
import drawObstaclesPath

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
NUM_WAYPOINTS = 4
NUM_OBSTACLE = 10
USE_GUI = True#Whether to enable the gui



waypoint_list, obstacle_list = fieldgen.fieldGen(FIELD_WIDTH, FIELD_HEIGHT,USE_GUI , NUM_OBSTACLE, NUM_WAYPOINTS)

paths = []  # append your paths to this list to draw them all at once (for comparison)
#paths.append(fanpath.extendingfan(obstacle_list, waypoint_list[0], waypoint_list[1]))
#qpaths.append(fanpath.simplefan(obstacle_list, waypoint_list[0], waypoint_list[1]))
paths.append(rubberpath.rubberpath(obstacle_list, waypoint_list,True,FIELD_HEIGHT,FIELD_WIDTH))

drawObstaclesPath.drawObstaclesPath(obstacle_list,paths,FIELD_HEIGHT,FIELD_WIDTH)