function [energyUsed] = GetEnergy(powers,times)
%GETENERGY This function integrates powers over times to get the total
%energy used
% Input;
%   powers: Array of the power used at each interval between the times
%   times: Array of the times corresponding to the segments around each
%   power
%
% Output
%   energyUsed: This is the total approximated energy to fly the course

energyUsed = trapz(times(1:end-1),powers);
end

