function [powers] = GetPower(thrusts,powercurve,vprofile)
%GETPOWER This calculates the power that is being used at each of the
%different time intervals
%   
% Input
%   thrusts: This is an array of how much thrust the craft needs to be
%   producing at each time segment
%   powercurves: This is a 2d retrieval array that contains the data for
%   the amount of power that is used at given values of thrust and velocity
%   of the craft(experimentally obtained)(y = velocity, x = thrust)
%   vprofile: This is an array of the velocities at evenly spaced time
%   intervals
%
% Output
%   powers: An array of the same length as thrusts outlining the amount of
%   power used at each time interval
powers = interp2(powercurve,thrusts+1,vprofile(1:end-1)+1);

end

