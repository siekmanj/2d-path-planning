function [vprofile] = ForwardAccCheck(vmax,veff,fc,r,dr)
% FORWARDACCCHECK This function will run through all of the vmax values, and
% will then go through and will accellerate the craft from a starting
% velocity of 0 and will create an velocity profile that attempts to
% converge to the most efficient velocity using the maximum allowed
% horizontal force as well as staying within the constraints of the
% previously established maximum velocity at each of the points
% 
% Input:
%   vmax: This is an array with all of the previously established maximum
%   velocities along the pat
%   veff: This is the pre-calculated most efficient speed
%   fc: A struct with the following atrributes
%       -thrust: Thrust in N
%       -mass: Mass of copter in kg
%       -density: Density of air in kg/m^3
%       -cd: Coefficient of drag for copter
%       -refarea: Drag reference area
%   r: This is an array of the radius of curvature along the path
%   dr: This is the arc length step
% 
% Output:
%   vprofile: This is the tangential velocity profile for the multicopter
%   to take over the path

g = 9.8;%m/s^2

vprofile = zeros(size(vmax));
fMaxHoriz = fc.thrust*cos(asin(fc.mass*g/fc.thrust))
%fMaxHoriz = fc.thrust;
%Iterate through all of the positions
for k = 1:length(vmax)-1
    %calculate the maximum tangential accelleration possible at this point
    amax = (sqrt(fMaxHoriz^2-(fc.mass*vprofile(k)^2/r(k))^2)-fc.cd*vprofile(k)^2*fc.density*fc.refarea/2 )/fc.mass;
    
    vnext = sqrt(vprofile(k).^2+2.*amax.*dr);
    %Check if either of the values are greater than the speed of greatest
    %efficiency, or if they are greater than the maximum flyable speed that
    %was input previously
    vprofile(k+1) = min([vmax(k+1),vnext,veff]);
end

%Really shouldn't need this, but some error in the numerical method means
%that there are some really small imaginary components because 
% fmax^2-(mCopter*vprofile(k)^2/r(k))^2 is greater than 0
vprofile=real(vprofile);

end

