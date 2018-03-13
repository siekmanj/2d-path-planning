function [arcLength] = NumericArcLength(x,y)
%NumericArcLength Calculates the numeric arc length for a set of x and y
%coords

arcLength = 0;

for k = 1:length(x)-1
    arcLength = arcLength + pdist([x(k),y(k);x(k+1),y(k+1)]);
end
end

