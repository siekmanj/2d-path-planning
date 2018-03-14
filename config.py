import configparser

CFG_FILE_NAME = 'config.ini'

cfg = configparser.ConfigParser()
cfg.read(CFG_FILE_NAME)

FIELD_WIDTH = int(cfg['general']['FieldWidth'])
FIELD_HEIGHT = int(cfg['general']['FieldHeight'])
NUM_WAYPOINTS = int(cfg['general']['NumWaypoints'])
NUM_OBSTACLE = int(cfg['general']['NumObstacles'])
NUM_BOUND_PTS = int(cfg['general']['NumBoundPoints'])#This should not be smaller than 3
SHOW_RUBBER_STEPS = cfg['rubberpath'].getboolean('UseRubberSteps')
USE_GUI = cfg['fieldGen'].getboolean('UseGUI') #Whether to enable the gui

FILENAME_PATHS = cfg['files']['Path']
FILENAME_WAYPOINTS = cfg['files']['Waypoint']
FILENAME_OBSTACLES = cfg['files']['Obstacle']
