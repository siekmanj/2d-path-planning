from position import *
from segment import Segment
import math
import random

SLOPE  = 6000
ATTRACTION = -.7
CONCAVITY = 50

MAX_SPEED = 1

#this kind of works sometimes
def simplegravity(obstacleList, waypointList, FIELD_HEIGHT, FIELD_WIDTH):
	currentpos = waypointList[0];
	segments = []
	xspd = 0
	yspd = 0
	for i in range(len(waypointList)-1):
		if not currentpos.distanceTo(waypointList[i+1]) == 0:
			for j in range(15000):
				start = currentpos
				xacc = 0;
				yacc = 0;
				#calculate attractive force to end position
				xspd += ATTRACTION * math.cos(currentpos.angle(waypointList[i+1]))# * (1/(currentpos.distanceTo(waypointList[i+1])**2))
				yspd += ATTRACTION * math.sin(currentpos.angle(waypointList[i+1]))# * (1/(currentpos.distanceTo(waypointList[i+1])**2))
				
				#calculate repulsive forces from obstacles, add the acceleration to the speed
				for obstacle in obstacleList:
					
					#SOMETHING WRONG WITH THIS LOGIC - POSSIBLY ANGLE FUNCTION
					if obstacle.distanceTo(currentpos) < 200:
						xacc += math.cos(currentpos.angle(obstacle.position)) * SLOPE/obstacle.distanceTo(currentpos)**2
						yacc += math.sin(currentpos.angle(obstacle.position)) * SLOPE/obstacle.distanceTo(currentpos)**2
						
				#calculate repulsive forces from walls (currently not working)
				if(inbounds(currentpos, FIELD_HEIGHT, FIELD_WIDTH)):
					xacc += CONCAVITY / ((currentpos.x - FIELD_WIDTH)**2)
					xacc += CONCAVITY / ((currentpos.x)**2)
					yacc += CONCAVITY / ((currentpos.y - FIELD_WIDTH)**2)
					yacc += CONCAVITY / ((currentpos.y)**2)
				else:
					print("OUT: (" + str(math.floor(currentpos.x)) + ", " + str(math.floor(currentpos.y)) + ")")
					if(currentpos is not waypointList[0]):
						print("Broke out of bounds, exiting.")
						break
				
				xspd += xacc
				yspd += yacc
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

#this is an attempt at a more sensible rewrite of simplegravity, hopefully with weird behavior
def bettergravity(obstacleList, waypointList, FIELD_HEIGHT, FIELD_WIDTH):
	before = waypointList[0]
	segments = []
	xSpeed = 0.0
	ySpeed = 0.0
	
	for waypoint in waypointList:
		if before is not waypoint:
			xPull = math.cos(before.angle(waypoint))
			yPull = math.sin(before.angle(waypoint))
			xSpeed += xPull
			ySpeed += yPull
			
			after = Position(before.x+xSpeed, before.y+ySpeed)
			segments.append(Segment(before, after))
			before = after	
	
	return segments
	
	
def inbounds(pos, FIELD_HEIGHT, FIELD_WIDTH):
	if(pos.x <= 0 or pos.x > FIELD_WIDTH or pos.y <= 0 or pos.y > FIELD_HEIGHT):
		return False
	return True

def limitSpeed(spd, low, high):
	if spd < low:
		return low
	if spd > high:
		return high
	return spd
