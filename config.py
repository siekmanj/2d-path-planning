import configparser
from PIL import Image
import numpy as np

CFG_FILE_NAME = 'config.ini'

cfg = configparser.ConfigParser()
cfg.read(CFG_FILE_NAME)

FIELD_WIDTH = int(cfg['general']['FieldWidth'])
FIELD_HEIGHT = int(cfg['general']['FieldHeight'])
NUM_WAYPOINTS = int(cfg['general']['NumWaypoints'])
NUM_OBSTACLE = int(cfg['general']['NumObstacles'])
NUM_BOUND_PTS = int(cfg['general']['NumBoundPoints'])#This should not be smaller than 3
NUM_SPLINE_PTS = int(cfg['general']['NumSplinePoints'])
AUTO_EXIT = cfg['general'].getboolean('AutoExit')
AUTO_EXIT_TIME_MS = int(cfg['general']['AutoExitTimeMS'])
SHOW_RUBBER_STEPS = cfg['rubberpath'].getboolean('UseRubberSteps')
USE_GUI = cfg['fieldGen'].getboolean('UseGUI') #Whether to enable the gui
USE_IMAGE_SIZE = cfg['fieldGen'].getboolean('UseImageSize') #Whether to use Image for sizing the screen

FILENAME_PATHS = cfg['files']['Path']
FILENAME_WAYPOINTS = cfg['files']['Waypoint']
FILENAME_OBSTACLES = cfg['files']['Obstacle']
FILENAME_MAPIMAGE = cfg['files']['MapImage']
FILENAME_MAPCOORDS = cfg['files']['MapCoords']

if USE_IMAGE_SIZE:
    im = Image.open(FILENAME_MAPIMAGE)
    FIELD_WIDTH, FIELD_HEIGHT = im.size


#Read in the data Vals
coords = np.loadtxt(FILENAME_MAPCOORDS,delimiter=',')
TOP_LATITUDE = coords[0]
LEFT_LONGITUDE = coords[1]
WIDTH_LONGITUDE = coords[1]-coords[3]
HEIGHT_LATITUDE = coords[0]-coords[2]
HEIGHT_METERS = coords[4]
WIDTH_METERS = FIELD_WIDTH/FIELD_HEIGHT * HEIGHT_METERS
SCALE_FACTOR = HEIGHT_METERS/FIELD_HEIGHT
