import writeFile
import config

def save_files(paths, waypoint_list, obstacle_list):

	writeFile.writeFile(config.FILENAME_PATHS, paths)
	writeFile.writeFile(config.FILENAME_WAYPOINTS, waypoint_list)
	writeFile.writeFile(config.FILENAME_OBSTACLES, obstacle_list)
