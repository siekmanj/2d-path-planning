function [times] = VelocitiesToTimes(vprofile,dr)
%VELOCITIESTOTIMES This function will take the velocities that are equally
%spaced out over the time and will then create the times that correspond to
%each of these points
%
% Input: 
%   vprofile: velocity profile of velocities evenly spaced by arc
%   length
%   dr: this is the length of an arc length step
%
% Output:
%   times: array of time values that correspond to each of the different
%   velocities in the profile

times = zeros(size(vprofile));

%Iterate through all of the velocities
for k = 2:length(vprofile)
    times(k) = times(k-1) + dr*1/trapz(vprofile(k-1:k));
end%end for
end

