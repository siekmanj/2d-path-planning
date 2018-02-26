import drawObstaclesPath
import readFile
import configparser

CFG_FILE_NAME = 'config.ini'

cfg = configparser.ConfigParser()
cfg.read(CFG_FILE_NAME)

FIELD_WIDTH = int(cfg['general']['FieldWidth'])
FIELD_HEIGHT = int(cfg['general']['FieldWidth'])


PathFileName = cfg['files']['Path']
WaypointFileName = cfg['files']['Waypoint']
ObstacleFileName = cfg['files']['Obstacle']

paths = readFile.readFile(PathFileName)
waypoint_list = readFile.readFile(WaypointFileName)
obstacle_list = readFile.readFile(ObstacleFileName)

drawObstaclesPath.drawObstaclesPath(obstacle_list,paths,FIELD_HEIGHT,FIELD_WIDTH)
