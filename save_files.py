import fieldgen
import fanpath
import rubberpath
import writeFile
import globalvars

def save_files():
  waypoint_list, obstacle_list = fieldgen.fieldGen(globalvars.FIELD_WIDTH, globalvars.FIELD_HEIGHT,globalvars.USE_GUI , globalvars.NUM_OBSTACLE, globalvars.NUM_WAYPOINTS)

  paths = []  # append your paths to this list to draw them all at once (for comparison)
  paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'simplefan', globalvars.FIELD_WIDTH, globalvars.FIELD_HEIGHT))
  paths.append(fanpath.multWaypointFan(obstacle_list,waypoint_list,'extendingfan', globalvars.FIELD_WIDTH, globalvars.FIELD_HEIGHT))
  paths.append(rubberpath.rubberpath(obstacle_list, waypoint_list,globalvars.SHOW_RUBBER_STEPS,globalvars.FIELD_HEIGHT,globalvars.FIELD_WIDTH))

  for p in range(len(paths)):
    for i in range(len(paths[p])):
      print('path {} segment {}: sx={}, sy={};\tex={}, ey={}'.format(p, i, paths[p][i].startPos.x, paths[p][i].startPos.y, paths[p][i].endPos.x, paths[p][i].endPos.y))


  writeFile.writeFile(globalvars.FILENAME_PATHS, paths)
  writeFile.writeFile(globalvars.FILENAME_WAYPOINTS, waypoint_list)
  writeFile.writeFile(globalvars.FILENAME_OBSTACLES, obstacle_list)
