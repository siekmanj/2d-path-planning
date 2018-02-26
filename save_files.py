import fieldgen
import fanpath
import rubberpath
import writeFile
import configparser

CFG_FILE_NAME = 'config.ini'

cfg = configparser.ConfigParser()
cfg.read(CFG_FILE_NAME)

FIELD_WIDTH = int(cfg['general']['FieldWidth'])
FIELD_HEIGHT = int(cfg['general']['FieldWidth'])
NUM_WAYPOINTS = int(cfg['general']['NumWaypoints'])
NUM_OBSTACLE = int(cfg['general']['NumObstacles'])
SHOW_RUBBER_STEPS = cfg['rubberpath'].getboolean('UseRubberSteps')
USE_GUI = cfg['fieldGen'].getboolean('UseGUI') #Whether to enable the gui


waypoint_list, obstacle_list = fieldgen.fieldGen(FIELD_WIDTH, FIELD_HEIGHT,USE_GUI , NUM_OBSTACLE, NUM_WAYPOINTS)

paths = []  # append your paths to this list to draw them all at once (for comparison)
paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'simplefan'))
paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'extendingfan'))
paths.append(rubberpath.rubberpath(obstacle_list, waypoint_list,SHOW_RUBBER_STEPS,FIELD_HEIGHT,FIELD_WIDTH))

for p in range(len(paths)):
  for i in range(len(paths[p])):
    print('path {} segment {}: sx={}, sy={};\tex={}, ey={}'.format(p, i, paths[p][i].startPos.x, paths[p][i].startPos.y, paths[p][i].endPos.x, paths[p][i].endPos.y))

PathFileName = cfg['files']['Path']
WaypointFileName = cfg['files']['Waypoint']
ObstacleFileName = cfg['files']['Obstacle']

writeFile.writeFile(PathFileName, paths)
writeFile.writeFile(WaypointFileName, waypoint_list)
writeFile.writeFile(ObstacleFileName, obstacle_list)
