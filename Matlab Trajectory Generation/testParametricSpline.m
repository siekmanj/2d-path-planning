clc 
clear

x = [50,100,150,120];%x values of spline control points
y = [150,20,25,100];%y values of spline control points

obs = [50,50;100,20];
obs_rad = [20,25];

pvf = linspace(0,100,100);

powercurve = repmat(pvf,length(pvf),1);

controlPts = [x,y];

waypoints = [0,0;200,200];

veff = 12;

%Flight Characteristics
fc = struct;
fc.thrust = 50;%N
fc.mass = 4;%kg
fc.density = 1.225;%kg/m^3
fc.cd = 1;%Coefficient of drag
fc.refarea = .25;%Reference area in m^2


energyused = GetEnergyPath(controlPts,waypoints,fc,1000,1,veff,powercurve,obs,obs_rad)

constraints(controlPts,250,waypoints,obs,obs_rad)

%fmincon testing
A = [];
b = [];
Aeq = [];
beq = [];

%Options pulled from other document
max_func_evals = 10000;
max_iter = 50000;
%options = optimoptions('fmincon','Algorithm','sqp','MaxFunEvals',max_func_evals,'MaxIter',max_iter,...
%        'GradObj','off','GradCon','off');

lb = zeros(size(controlPts));
ub = ones(size(controlPts))*300;

cons = @(pts) constraints(pts,250,waypoints,obs,obs_rad);
opt_e = @(pts) GetEnergyPath(pts,waypoints,fc,1000,0,veff,powercurve,obs,obs_rad);

optimized_pts = fmincon(opt_e,controlPts,A,b,Aeq,beq,lb,ub,cons);

energyused = GetEnergyPath(optimized_pts,waypoints,fc,1000,1,veff,powercurve,obs,obs_rad)
constraints(optimized_pts,250,waypoints,obs,obs_rad)

