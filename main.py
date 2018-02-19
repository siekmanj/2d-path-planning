import fieldgen
import fanpath
import rubberpath
import drawObstaclesPath

FIELD_WIDTH = 1000
FIELD_HEIGHT = 600
NUM_WAYPOINTS = 2
NUM_OBSTACLE = 10
SHOW_RUBBER_STEPS = False
USE_GUI = True#Whether to enable the gui



waypoint_list, obstacle_list = fieldgen.fieldGen(FIELD_WIDTH, FIELD_HEIGHT,USE_GUI , NUM_OBSTACLE, NUM_WAYPOINTS)

paths = []  # append your paths to this list to draw them all at once (for comparison)
paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'simplefan'))
paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'extendingfan'))
paths.append(rubberpath.rubberpath(obstacle_list, waypoint_list,SHOW_RUBBER_STEPS,FIELD_HEIGHT,FIELD_WIDTH))

drawObstaclesPath.drawObstaclesPath(obstacle_list,paths,FIELD_HEIGHT,FIELD_WIDTH)