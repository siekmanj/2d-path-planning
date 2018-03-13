function [c,ceq] = constraints(controlPts,numPoints,waypoints,obs,rad_obs)
%Constraints: This function will take in the control points and will then
% return -1 if there are intersections, or 0 if there are intersections
%
% This function will then be called inside of the fmincon function and thus
% it will reutrn a negative if the constraints are not violated and a
% positive if the constraints are violated
c = [];
ceq = [];
disp(c);

controlPts = [waypoints(1,1),controlPts(1:end/2),waypoints(2,1);waypoints(1,2),controlPts(end/2+1:end),waypoints(2,2)];

[pathPolys,arcParams,~,~] = InterpWaypoints(controlPts,numPoints);

pathPoints = [ppval(pathPolys(1),arcParams);ppval(pathPolys(2),arcParams)];

distEdge = [];

for k = 1:length(obs)
    distEdge(k,:) = sqrt((obs(k,1)-pathPoints(1,:)).^2+(obs(k,2)-pathPoints(2,:)).^2)-rad_obs(k);
end

c = -10.*distEdge;
end

