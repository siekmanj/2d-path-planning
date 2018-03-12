function [energyUsed] = GetEnergyPath(controlPts,waypoints,fc,numPoints,draw,veff,powercurve,obs,obs_rad)
%GetEnergyPath: This function will calculate the amount of energy for a
%given path
%   Inputs:
%   
%   controlPts: Array with the movable control points of path
%   waypoints: Array with the waypoints copter must go throught
%   fc: A struct with the following atrributes
%       -thrust: Thrust in N
%       -mass: Mass of copter in kg
%       -density: Density of air in kg/m^3
%       -cd: Coefficient of drag for copter
%       -refarea: Drag reference area
%   draw: boolean of whether to show the path
%   veff: velocity of highest efficiency
%
%   Output: 
%
%   energyUsed: energy used in flying path in wH
%
%   Steps:
%   1. Point interpolation to find discretized array of path points
%   2. Calculate curvature with respect to distance k(x)
%   3. Find vmax(s): max velocity as a function of arc length
%   4. Run Backward accelleration check
%   5. Run forward accelleration filter
%   6. Integrate dx/v(x) for each discretized point to find time for each
%   7. Solve for k(t) by substituting in x(t) into k(x)
%   8. Solve for Fthrust(t)
%   9. Use Fthrust to solve for P(t) 
%   10. Integrate P(t) over time interval of flight to get the energy used
%   11. If draw then plot all of the info

energyUsed = 0;
clf
close all

controlPts = [waypoints(1,1),controlPts(1:end/2),waypoints(2,1);waypoints(1,2),controlPts(end/2+1:end),waypoints(2,2)]
%Step 1
[pathPolys,arcParams,dr,r] = InterpWaypoints(controlPts,numPoints);
figure
if draw
    plot(ppval(pathPolys(1),arcParams),ppval(pathPolys(2),arcParams),'.r');
    hold on;
    t = linspace(0,2*pi,20);
    xc = cos(t);
    yc = sin(t);
    for j = 1:length(obs)
        %plot(obs(j,1)+xc*obs_rad(j),obs(j,2)+yc*obs_rad(j),'-r')
        hold on
    end
    axis equal
end

%Step 2
radCurvature_r = GetRadCurvature(pathPolys,arcParams);

%Step 3
vmax_r = GetMaxVelocity(radCurvature_r,fc);
if draw
    figure
    plot(r,vmax_r,'-b')
    title('Max velocity such that craft can still corner')
end

%Step 4
vmax_r = BackAccCheck(vmax_r,fc,dr);
if draw
    figure
    plot(r,vmax_r,'-r');
    title('Back Acc Check')
end
    
%Step 5
vprofile = ForwardAccCheck(vmax_r,veff,fc,radCurvature_r,dr);
if draw
    figure
    plot(r,vprofile,'-r');
    title('Forward Acc Check')
end
    
%Step 6
%times is an array corresponding to each velocity value along the path with
%the time at that point
times = VelocitiesToTimes(vprofile,dr);
if draw
    figure
    plot(times,vprofile,'-k')
    title('Velocity vs time')
end
    
%Step 7
%Already have this, as the radCurvature_r values correspond to the time
%vals

%Step 8
thrusts = GetThrusts(radCurvature_r,vprofile,times,fc,powercurve);
if draw
    figure
    plot(times(1:end-1),thrusts,'-g')
    title('Thrust v time')
end
    
%Step 9
powers = GetPower(thrusts,powercurve,vprofile);

if draw
    figure
    plot(times(1:end-1),powers,'-g')
    title('power vs time')
end
%Step 10
energyUsed = GetEnergy(powers,times);

end

