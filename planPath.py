import pathToPoints
import ProfilePath
import numpy as np
import tanDjikstra

def planPath(algorithm,obstacle_list,waypoint_list,bound_segments,curr_pos,fc,config):

    waypoint_list.insert(0,curr_pos)
    #switch statement for the algorithms
    if algorithm == 'tandji':
        #Tangent Djikstra
	#why is tangentDjikstra called again here? Shouldn't we just pass realpath from the previous invocation?
        realpath, _,_ = tanDjikstra.tangentDjikstra(waypoint_list, obstacle_list, bound_segments)
    else:
        print('That was not one of the options given so the default will be used')
        realpath, _, _ = tanDjikstra.tangentDjikstra(waypoint_list, obstacle_list, bound_segments)
    #-----------Motion Profiling Section--------------
    pathWaypoints = pathToPoints.pathToPoints(realpath)#Convert to simply the points

    #Eventually the powercurve will need to be some experimetnally obtained data
    pvf = np.linspace(0,100,100)

    powercurve = np.tile(pvf, (len(pvf),1))

    _,times,vprofile,points = ProfilePath.ProfilePath(pathWaypoints,fc,config.NUM_SPLINE_PTS,powercurve,config.SCALE_FACTOR)

    #Rescale the points to the GPS Scale

    posTimes = np.zeros((4,len(points)))
    posTimes[0,:] = config.LEFT_LONGITUDE - (config.WIDTH_LONGITUDE/config.WIDTH_METERS)*points[:,0]
    posTimes[1,:] = config.TOP_LATITUDE - (config.HEIGHT_LATITUDE/config.HEIGHT_METERS)*points[:,1]
    posTimes[2,:] = vprofile
    posTimes[3,:] = times
    return posTimes
