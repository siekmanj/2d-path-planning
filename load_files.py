import drawObstaclesPath
import readFile
import config

def load_files():
	paths = readFile.readFile(globalvars.FILENAME_PATHS)
	waypoint_list = readFile.readFile(globalvars.FILENAME_WAYPOINTS)
	obstacle_list = readFile.readFile(globalvars.FILENAME_OBSTACLES)

	drawObstaclesPath.drawObstaclesPath(obstacle_list, paths,globalvars.FIELD_HEIGHT, globalvars.FIELD_WIDTH)
