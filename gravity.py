from position import *
from segment import Segment
import math
import random

SLOPE  = 30
ATTRACTION = -1
CONCAVITY = 50

MAX_SPEED = 10

FIELD_HEIGHT = 600
FIELD_WIDTH = 1000

#this kind of works sometimes
def simplegravity(obstacleList, waypointList):
	currentpos = waypointList[0];
	segments = []
	xspd = 0
	yspd = 0
	for i in range(len(waypointList)-1):
		if not currentpos.distanceTo(waypointList[i+1]) == 0:
			for j in range(1500):
				start = currentpos
				#calculate attractive force to end position
				xspd += ATTRACTION * math.cos(currentpos.angle(waypointList[i+1]))# * (1/(currentpos.distanceTo(waypointList[i+1])**2))
				yspd += ATTRACTION * math.sin(currentpos.angle(waypointList[i+1]))# * (1/(currentpos.distanceTo(waypointList[i+1])**2))
				
				#calculate repulsive forces from obstacles, add the acceleration to the speed
				for obstacle in obstacleList:
					xacc = 0 
					yacc = 0
					
					#SOMETHING WRONG WITH THIS LOGIC - POSSIBLY ANGLE FUNCTION
					if obstacle.distanceTo(currentpos) < 200:
						xacc = math.cos(currentpos.angle(obstacle.position)) * SLOPE/obstacle.distanceTo(currentpos)
						yacc = math.sin(currentpos.angle(obstacle.position)) * SLOPE/obstacle.distanceTo(currentpos)
					xspd += xacc
					yspd += yacc
						
				#calculate repulsive forces from walls (currently not working)
				if(inbounds(currentpos)):
					xspd += CONCAVITY / ((currentpos.x - FIELD_WIDTH)**2)
					xspd += CONCAVITY / ((currentpos.x)**2)
					yspd += CONCAVITY / ((currentpos.y - FIELD_WIDTH)**2)
					yspd += CONCAVITY / ((currentpos.y)**2)
				else:
					print("OUT: (" + str(math.floor(currentpos.x)) + ", " + str(math.floor(currentpos.y)) + ")")
					if(currentpos is not waypointList[0]):
						print("Broke out of bounds, exiting.")
						break
				
				xspd = limitSpeed(xspd, -math.fabs(MAX_SPEED * math.cos(currentpos.angle(waypointList[i+1]))), math.fabs(MAX_SPEED * math.cos(currentpos.angle(waypointList[i+1]))))
				yspd = limitSpeed(yspd, -math.fabs(MAX_SPEED * math.sin(currentpos.angle(waypointList[i+1]))), math.fabs(MAX_SPEED * math.sin(currentpos.angle(waypointList[i+1]))))
				
				print(str(xspd) + ", " + str(yspd))
				
				end = Position(currentpos.x + xspd, currentpos.y + yspd)
				segments.append(Segment(start, end))
				currentpos = end
				if(currentpos.distanceTo(waypointList[i+1]) < 50):
					print("CLOSE ENOUGH")
					break
	return segments

def inbounds(pos):
	if(pos.x <= 0 or pos.x > FIELD_WIDTH or pos.y <= 0 or pos.y > FIELD_HEIGHT):
		return False
	return True

def limitSpeed(spd, low, high):
	if spd < low:
		return low
	if spd > high:
		return high
	return spd
