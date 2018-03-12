function [pathPolys,arcLengthParameters,dr,r] = InterpWaypoints(control_pts,numPoints)
%InterpWaypoints This function will compute a spline from the given control
%points and will then calculate points for the function that are
%parametrized by arc length equally.
%
% Input:
%   control_pts: array of the control points with row 1 is x and row 2 is y
%   numPoints: The number of points that are used for the interpolation
%
% Output: 
%   pathPolys: This is an array of the piecewise polynomial structure of
%   the pchip spline fit
%   arcLengthParameters: Array of the parameter values that correspond to
%   equal arc length of the functions
%   dr: The arc length step

%Create the starting parameter values to correspond with x and y
control_s =  linspace(0,numPoints,length(control_pts));
%Define array of the parameters that will be used in the spline
%interpolation
s = [0:numPoints];

%Fit spline to initial arbitrary parameter
xPath = spline(control_s,control_pts(1,:));
yPath = spline(control_s,control_pts(2,:));
pathPolys = [xPath,yPath];
xs = ppval(xPath,s);
ys = ppval(yPath,s);

xy_s = [xs;ys];

%Calculate the tota distance of the path
distance = NumericArcLength(xs,ys);

%Create an array of the arc length parameter spaced evenly between zero and
%the final point
r = linspace(0,distance,numPoints);
dr = distance/numPoints;

%Calculate the values of s needed to evenly distribute points on arc length
arcLengthParameters = pdearcl(s,xy_s,r,0,distance);


end

