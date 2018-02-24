from position import *
from segment import Segment
import math
import random

REPULSION  = 75
ATTRACTION = 400000

FIELD_HEIGHT = 600
FIELD_WIDTH = 1000


def simplegravity(obstacleList, waypointList):
	currentpos = waypointList[0];
	segments = []
	for i in range(len(waypointList)-1):
		if not currentpos.distanceTo(waypointList[i+1]) == 0:
			for j in range(150):
				start = currentpos
				#calculate attractive force to end position
				xforce = ATTRACTION * math.cos(currentpos.angle(waypointList[i])) * (1/(currentpos.distanceTo(waypointList[i+1])**2))
				yforce = ATTRACTION * math.sin(currentpos.angle(waypointList[i])) * (1/(currentpos.distanceTo(waypointList[i+1])**2))
				
				#calculate repulsive forces from obstacles
				for obstacle in obstacleList:
					xforce += REPULSION * math.cos(currentpos.angle(obstacle.position)) * (1/(currentpos.distanceTo(obstacle.position)**2))
					yforce += REPULSION * math.sin(currentpos.angle(obstacle.position)) * (1/(currentpos.distanceTo(obstacle.position)**2))
					
				#calculate repulsive forces from walls (currently not working)
				xforce += REPULSION * (FIELD_WIDTH/2 + currentpos.x)**2
				yforce += REPULSION * (FIELD_HEIGHT/2 + currentpos.y)**2
				
				end = Position(currentpos.x + xforce, currentpos.y + yforce)
				segments.append(Segment(start, end))
				currentpos = end
	return segments

             
