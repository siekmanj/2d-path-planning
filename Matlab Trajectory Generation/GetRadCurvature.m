function [radCurvature] = GetRadCurvature(pathPolys,arcParams)
% GETRADCURVATURE This function will numerically calculate the radius of
% curvature of the path at all of the given points, and will then output
% that value
% 
% Inputs:
%   pathPolys: parametric x and y piecewise polynomials for path
%   arcParams: the parameter values for equal arc length
% 
% Outputs: 
%   radCurvature: Array of the radius of curvature(make sure it is the same length)

x = ppval(pathPolys(1),arcParams);
y = ppval(pathPolys(2),arcParams);

dx = ppval(fnder(pathPolys(1),1),arcParams);
dy = ppval(fnder(pathPolys(2),1),arcParams);

ddx = ppval(fnder(pathPolys(1),2),arcParams);
ddy = ppval(fnder(pathPolys(2),2),arcParams);

%Calculate the curvature
k = (abs(dx.*ddy-ddx.*dy))./(dx.^2+dy.^2).^(3/2);

k(k == 0) = .00001;

%Calculate the radius of curvature
radCurvature = 1./k;

end

