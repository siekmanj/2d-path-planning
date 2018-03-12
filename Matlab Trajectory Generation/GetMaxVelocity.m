function [vmax] = GetMaxVelocity(radCurvature,fc)
%GETMAXVELOCITY This function will calculate the maximum velocity that the
%UAV can fly such that the maximum force is still sufficient to provide the
% centripetal force required as a function of the curvature
%
% Input:
%   radCurvature: array with the radius of curvature at each of the
%       points parametrized by arc length
%   fc: A struct with the following atrributes
%       -thrust: Thrust in N
%       -mass: Mass of copter in kg
%       -density: Density of air in kg/m^3
%       -cd: Coefficient of drag for copter
%       -refarea: Drag reference area

%Parameters
g = 9.8;%m/s^2

%Calculate the maximum horizontal force that the quadcopter can apply
fMaxHoriz = fc.thrust*cos(asin(fc.mass*g/fc.thrust));

%Calculate the maximum velocity as a function of the arc length
vmax = sqrt(fMaxHoriz.*radCurvature./fc.mass);%m/s
end

