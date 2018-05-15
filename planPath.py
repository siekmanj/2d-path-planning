import pathToPoints
import ProfilePath
import numpy as np
import tanDjikstra

def planPath(algorithm,obstacle_list,waypoint_list,bound_segments,curr_pos,fc,config):

    waypoint_list.insert(0,curr_pos)
    #switch statement for the algorithms
    if algorithm == 'tandji':
        #Tangent Djikstra
        realpath, _,_ = tanDjikstra.tangentDjikstra(waypoint_list, obstacle_list, bound_segments)
    else:
        print('That was not one of the options given so the default will be used')
        realpath, _, _ = tanDjikstra.tangentDjikstra(waypoint_list, obstacle_list, bound_segments)
    #-----------Motion Profiling Section--------------
    pathWaypoints = pathToPoints.pathToPoints(realpath)#Convert to simply the points

    #Eventually the powercurve will need to be some experimetnally obtained data
    pvf = np.linspace(0,100,100)

    powercurve = np.tile(pvf, (len(pvf),1))

    _,times,vprofile,points = ProfilePath.ProfilePath(pathWaypoints,fc,config.NUM_SPLINE_PTS,powercurve)

    posTimes = np.zeros((3,len(points)))
    posTimes[0,:] = points[:,0]
    posTimes[1,:] = points[:,1]
    posTimes[2,:] = times
    return posTimes