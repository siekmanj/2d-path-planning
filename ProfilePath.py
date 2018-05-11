import matplotlib
import numpy as np
import scipy.interpolate
import scipy.misc
import scipy
import interparc
import matplotlib.pyplot as plt
import math


def ProfilePath(waypoints,fc,numPoints,powercurve):
    #GetEnergyPath: This function will calculate the amount of energy for a
    #given path
    #   Inputs:
    #
    #   waypoints: Array with the waypoints copter must go through in the form of x and y
    #   fc: A dictionary
    #       -thrust: Thrust in N
    #       -mass: Mass of copter in kg
    #       -density: Density of air in kg/m^3
    #       -cd: Coefficient of drag for copter
    #       -refarea: Drag reference area
    #       -veff: most efficient velocity that the path planning software will attempt to converge to
    #   draw: boolean of whether to show the path
    #   powercurve:
    #
    #   Output: 
    #
    #   energyUsed: energy used in flying path in wH
    #
    #   Steps:
    #   1. Point interpolation to find discretized array of path points
    #   2. Calculate curvature with respect to distance k(x)
    #   3. Find vmax(s): max velocity as a function of arc length
    #   4. Run Backward accelleration check
    #   5. Run forward accelleration filter
    #   6. Integrate dx/v(x) for each discretized point to find time for each
    #   7. Solve for k(t) by substituting in x(t) into k(x)
    #   8. Solve for Fthrust(t)
    #   9. Use Fthrust to solve for P(t) 
    #   10. Integrate P(t) over time interval of flight to get the energy used
    #   11. If draw then plot all of the info

    #Scale the field from px to meters
    waypoints = waypoints/10

    #Step 1
    pathPolys,arcParams,dr,r,points = InterpWaypoints(waypoints,numPoints);
    #plt.plot(pathPolys[0](arcParams),pathPolys[1](arcParams))
    #plt.plot(arcParams,pathPolys[0](arcParams))
    x = points[:,0]
    y = points[:,1]
    plt.plot(x,y,'.b')

    #Step 2
    radCurvature = GetRadCurvature(x,y)
    #plt.plot(np.linspace(0,700,len(radCurvature)),radCurvature)
    #Step 3
    vmax = GetMaxVelocity(radCurvature,fc)
    plt.plot(np.linspace(0,700,len(vmax)),vmax)

    #Step 4
    vmax = BackAccCheck(vmax,fc,dr)
    plt.plot(np.linspace(0,700,len(vmax)),vmax)

    #Step 5
    vprofile = ForwardAccCheck(vmax,fc,radCurvature,dr)
    plt.plot(np.linspace(0,700,len(vmax)),vprofile)

    #Step 6
    times = VelocitiesToTimes(vprofile,dr)

    #Step 7
    #already have

    #Step 8
    thrusts = GetThrusts(radCurvature,vprofile,times,fc)
    plt.plot(np.linspace(0,700,len(radCurvature)-1),thrusts)
    plt.figlegend('test')

    #Step 9
    powers = GetPower(thrusts,powercurve,vprofile)

    #Step 10
    energyUsed = GetEnergy(powers,times)

    return energyUsed,times,vprofile,points


def InterpWaypoints(waypoints,numPoints):
    #InterpWaypoints This function will compute a spline from the given control
    #points and will then calculate points for the function that are
    #parametrized by arc length equally.
    #
    # Input:
    #   control_pts: array of the control points with row 1 is x and row 2 is y
    #   numPoints: The number of points that are used for the interpolation
    #
    # Output: 
    #   pathPolys: This is an array of the piecewise polynomial structure of
    #   the pchip spline fit
    #   arcLengthParameters: Array of the parameter values that correspond to
    #   equal arc length of the functions
    #   dr: The arc length step
    
    #Create the starting parameter values to correspond with x and y
    control_s =  np.linspace(0,numPoints,waypoints.shape[1])
    control_s = control_s.transpose()
    #Define array of the parameters that will be used in the spline
    #interpolation
    s = np.arange(numPoints)
    x = waypoints[0,:].transpose()
    y = waypoints[1,:].transpose()
    xshape = x.shape
    yshape = y.shape
    contrlshape = control_s.shape
    #Fit spline to initial arbitrary parameter
    xPath = scipy.interpolate.PchipInterpolator(control_s, x)
    yPath = scipy.interpolate.PchipInterpolator(control_s, y)
    pathPolys = [xPath,yPath]
    xs = xPath(s)
    ys = yPath(s)
    distance = NumericArcLength(xs, ys);
    dr = distance/numPoints
    r = np.linspace(0,distance,numPoints);

    #Definitely not the most efficient wey to do this since it is recalculating the spline, fit, but for now it is ok
    #Interpolate evenly spaced points along the spline
    points, arcLengthParams = interparc.interparc(numPoints,x,y,'linear')

    #Rescale the arclength params from  1 to the whole distance of the path

    arcLengthParams = np.sort(arcLengthParams)

    arcLengthParams = np.multiply(arcLengthParams, numPoints)

    return pathPolys,arcLengthParams,dr,r,points

def GetRadCurvature(x,y):

    #Take the first derivatives of the splines at the evenly spaced points by arc length
    dx = np.diff(x)
    dy = np.diff(y)
    dx = np.append(dx, dx[-1])
    dy = np.append(dy, dy[-1])

    plt.plot(np.linspace(0, 700, len(dx)), dx)
    plt.plot(np.linspace(0, 700, len(dy)), dy)
    # Take the second derivatives of the splines at the evenly spaced points by arc length
    ddx = np.diff(dx)
    ddy = np.diff(dy)
    ddx = np.append(ddx, ddx[-1])
    ddy = np.append(ddy, ddy[-1])
    plt.plot(np.linspace(0, 700, len(ddx)), ddx)
    plt.plot(np.linspace(0, 700, len(ddy)), ddy)


    #denominator of the k equation

    k = (abs(dx * ddy - ddx * dy)) / ((dx ** 2 + dy ** 2) ** (3 / 2))
    #Make sure that there are not any 0 values left
    k[k == 0] = .00001

    #Calculate the radius of curvature
    radCurvature = 1/k

    radCurvature[radCurvature > 100000] = 100000
    return radCurvature

def GetMaxVelocity(radCurvature, fc):
    # GETMAXVELOCITY This function will calculate the maximum velocity that the
    # UAV can fly such that the maximum force is still sufficient to provide the
    # centripetal force required as a function of the curvature
    #
    # Input:
    #   radCurvature: array with the radius of curvature at each of the
    #       points parametrized by arc length
    #   fc: A dictionary with the following elements
    #       -thrust: Thrust in N
    #       -mass: Mass of copter in kg
    #       -density: Density of air in kg/m^3
    #       -cd: Coefficient of drag for copter
    #       -refarea: Drag reference area
    #
    # Output
    #   vmax: This is an array of the maximum velocities the drone can fly at
    #   based on turning at each point

    #Gravity
    g = 9.8

    #Calculate the maximum horizontal force that the copter can supply while maintaining altitude disregarding any lift
    fMaxHoriz = fc["thrust"]*np.cos(np.arcsin(fc["mass"]*g/fc["thrust"]))
    #Put a buffer to create nan protection in forwawrd acc check
    fMaxHoriz = fMaxHoriz*.90

    vmax = np.sqrt(fMaxHoriz*radCurvature/fc["mass"])
    return vmax

def BackAccCheck(vmaxIn,fc,dr):
    # BACACCCHECK This function will filter the max velocity profile backwards
    #   The goal of this function is to ensure that the vmax velocity profile
    #   for the multicopter never has a negative slope(acceleration), greater
    #   than air resistance is able to provide at that speed such that the
    #   multicopter will never be have to reverse thrust
    #
    # Input:
    #   vmaxIn:This is an array of the max allowable velocity values such that
    #   the mutlicopter has the capability to corner.
    #   dr: This is the distance step between each of the individual velocity
    #   values
    #   fc: A dictionary with the following atrributes
    #       -thrust: Thrust in N
    #       -mass: Mass of copter in kg
    #       -density: Density of air in kg/m^3
    #       -cd: Coefficient of drag for copter
    #       -refarea: Drag reference area
    #
    # Output
    #   vmaxOut:Array in the same form of vmaxIn after the filter has been run
    vmax = vmaxIn

    for i in range(len(vmaxIn)-1,1,-1):
        vcurr = vmax[i]

        vprevmax = np.sqrt(vcurr ** 2 + fc["cd"] * fc["density"] * fc["refarea"] * dr * vcurr ** 2 / fc["mass"])

        if vmax[i - 1] > vprevmax:
            vmax[i-1] = vprevmax

    return vmax

def ForwardAccCheck(vmax,fc,r,dr):
    # FORWARDACCCHECK This function will run through all of the vmax values, and
    # will then go through and will accellerate the craft from a starting
    # velocity of 0 and will create an velocity profile that attempts to
    # converge to the most efficient velocity using the maximum allowed
    # horizontal force as well as staying within the constraints of the
    # previously established maximum velocity at each of the points
    #
    # Input:
    #   vmax: This is an array with all of the previously established maximum
    #   velocities along the pat
    #   veff: This is the pre-calculated most efficient speed
    #   fc: A struct with the following atrributes
    #       -thrust: Thrust in N
    #       -mass: Mass of copter in kg
    #       -density: Density of air in kg/m^3
    #       -cd: Coefficient of drag for copter
    #       -refarea: Drag reference area
    #   r: This is an array of the radius of curvature along the path
    #   dr: This is the arc length step
    #
    # Output:
    #   vprofile: This is the tangential velocity profile for the multicopter
    #   to take over the path
    g = 9.8
    vprofile = np.zeros(vmax.shape)
    fMaxHoriz = fc["thrust"]*np.cos(np.arcsin(fc["mass"]*g/fc["thrust"]))

    #Iterate through all of the positions
    for i in range(len(vmax)-1):
        amax = (np.sqrt(fMaxHoriz ** 2 - (fc["mass"] * vprofile[i] ** 2 / r[i]) ** 2) - fc["cd"] * vprofile[i] ** 2 * fc["density"] * fc["refarea"] / 2) / fc["mass"]
        vnext = np.sqrt(vprofile[i] ** 2 + 2 * amax * dr)
        if math.isnan(amax) or math.isnan(vnext):
            print('We have  an issue')

        #The actual value of the speed for that point should be the minimum out of the following 3 options
        vprofile[i + 1] = np.min(np.array((vnext,fc["veff"],vmax[i+1])))

    #Really shouldn't need this, but some error in the numerical method means
    #that there are some really small imaginary components because
    # fmax^2-(mCopter*vprofile(k)^2/r(k))^2 is greater than 0
    vprofile = np.real(vprofile)

    return vprofile

def VelocitiesToTimes(vprofile,dr):
    #VELOCITIESTOTIMES This function will take the velocities that are equally
    #spaced out over the time and will then create the times that correspond to
    #each of these points
    #
    # Input:
    #   vprofile: velocity profile of velocities evenly spaced by arc
    #   length
    #   dr: this is the length of an arc length step
    #
    # Output:
    #   times: array of time values that correspond to each of the different
    #   velocities in the profile
    times = np.zeros(vprofile.size)

    for i in range(1,len(vprofile)):
        times[i] = times[i-1] + dr * 1 / np.trapz(vprofile[i-1:i+1])

    return times

def GetThrusts(radCurvature, vprofile, times, fc):
    #GETTHRUSTS This function will take in arrays with the velocity profile as
    #well as the radius of curvature at each of the given points. Then it takes
    #this data and will calculate the needed horizontal 2d force that is
    #required to attain/maintain these speeds and will then add the required
    #vertical component to remain stable in the z direction and will output the
    #thrust force required at each point
    #
    # Input:
    #   radCurvature: This is an array of the radius of curvature at all of the
    #   given points
    #   vprofile: This is an array of the velocity at all of the given points
    #   fc: Flight Characteristics
    #   powercurv2: This is a 2d array that contains all of the different power
    #   usages to obtain a certain thrust at a give velocity
    #
    # Output:
    #   thrusts: This is an array of the thrusts(NOTE: this will be one shorter than the input arrays)
    thrusts = np.ones(len(vprofile)-1)
    g = 9.8
    #Iterate through the segments
    for i in range(len(vprofile)-1):
        a = (vprofile[i+1]-vprofile[i])/(times[i+1]-(times[i]))
        fd = vprofile[i] ** 2 * fc["cd"] * fc["density"] * fc["refarea"] / 2
        fcp = fc["mass"] * vprofile[i] ** 2 / radCurvature[i]; #Centripetal Force

        thrusts[i] = np.sqrt((fc["mass"] * a + fd) ** 2 + fcp ** 2 + (fc["mass"]*g) ** 2)

    return thrusts

def GetPower(thrusts,powercurve,vprofile):
    #GETPOWER This calculates the power that is being used at each of the
    #different time intervals
    #
    # Input
    #   thrusts: This is an array of how much thrust the craft needs to be
    #   producing at each time segment
    #   powercurves: This is a 2d retrieval array that contains the data for
    #   the amount of power that is used at given values of thrust and velocity
    #   of the craft(experimentally obtained)(y = velocity, x = thrust)
    #   vprofile: This is an array of the velocities at evenly spaced time
    #   intervals
    #
    # Output
    #   powers: An array of the same length as thrusts outlining the amount of
    #   power used at each time interval
    '''vpoints = np.linspace(0,100,len(powercurve));
    tpoints = np.linspace(0,110,len(powercurve));
    points = np.ones((len(powercurve),2))
    points[:,0] = vpoints
    points[:,1] = tpoints

    powers = scipy.interpolate.griddata(points,powercurve,(thrusts + 1, vprofile[0:-1]+1))
    '''
    #temporary until grid interpolation works
    powers = thrusts*2

    return powers

def GetEnergy(powers,times):
    #GETENERGY This function integrates powers over times to get the total
    #energy used
    # Input;
    #   powers: Array of the power used at each interval between the times
    #   times: Array of the times corresponding to the segments around each
    #   power
    #
    # Output
    #   energyUsed: This is the total approximated energy to fly the course

    energyUsed = np.trapz(powers,times[0:-1])

    return energyUsed

def NumericArcLength(xs,ys):
    arcLength = 0

    for i in range(0,len(xs)-1):
        a = np.array((xs[i],ys[i]))
        b = np.array((xs[i+1],ys[i+1]))
        arcLength += np.linalg.norm(a-b)

    return arcLength

    
    



