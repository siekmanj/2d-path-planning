function [vmaxOut] = BackAccCheck(vmaxIn,fc,dr)
%BACACCCHECK This function will filter the max velocity profile backwards
%   The goal of this function is to ensure that the vmax velocity profile
%   for the multicopter never has a negative slope(acceleration), greater
%   than air resistance is able to provide at that speed such that the
%   multicopter will never be have to reverse thrust
%
% Input:
%   vmaxIn:This is an array of the max allowable velocity values such that
%   the mutlicopter has the capability to corner.
%   dr: This is the distance step between each of the individual velocity
%   values
%   fc: A struct with the following atrributes
%       -thrust: Thrust in N
%       -mass: Mass of copter in kg
%       -density: Density of air in kg/m^3
%       -cd: Coefficient of drag for copter
%       -refarea: Drag reference area
%
% Output
%   vmaxOut:Array in the same form of vmaxIn after the filter has been run

vmaxOut = vmaxIn;
%Iterate backwards through the array running the filter
for k = length(vmaxIn):-1:2
    vcurr = vmaxOut(k);%Current velocity
    
    vprevmax = sqrt(vcurr^2+fc.cd*fc.density*fc.refarea*dr*vcurr^2/fc.mass);%max allowed so no reverse thrust used
    
    %Check if the previous one is greater than the max it is allowed to be
    if vmaxOut(k-1) > vprevmax
        vmaxOut(k-1) = vprevmax;
    end
end

