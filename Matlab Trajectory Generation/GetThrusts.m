function [thrusts] = GetThrusts(radCurvature,vprofile,times,fc,powercurve)
%GETTHRUSTS This function will take in arrays with the velocity profile as
%well as the radius of curvature at each of the given points. Then it takes
%this data and will calculate the needed horizontal 2d force that is
%required to attain/maintain these speeds and will then add the required
%vertical component to remain stable in the z direction and will output the
%thrust force required at each point
%
% Input: 
%   radCurvature: This is an array of the radius of curvature at all of the
%   given points
%   vprofile: This is an array of the velocity at all of the given points
%   fc: Flight Characteristics
%   powercurv2: This is a 2d array that contains all of the different power
%   usages to obtain a certain thrust at a give velocity
%
% Output: 
%   thrusts: This is an array of the thrusts(NOTE: this will be one shorter than the input arrays)

thrusts = ones(1,length(vprofile)-1);

%Iterate through the segments
for k = 1:length(vprofile)-1
    a = (vprofile(k+1)-vprofile(k))/(times(k+1)-(times(k)));
    fd = vprofile(k)^2*fc.cd*fc.density*fc.refarea/2;
    fcp = fc.mass*vprofile(k)^2/radCurvature(k);%Centripetal Force
    
    thrusts(k) = sqrt((fc.mass*a+fd)^2+fcp^2);
end

end

