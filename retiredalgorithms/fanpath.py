from position import *
from segment import *
import math
import random

def multWaypointFan(obstacleList,waypointList,algorithm,width,height):
	#This function will just iterate over the other fan functions and allow for multiple waypoints to be used
	overallPath = []
	for i in range(len(waypointList)-1):
		#iterate through all of the waypoint segments
		if algorithm == 'simplefan':
			#This should extend the overall path by the result ofo the simple fan algorithm between the two current waypoints
			overallPath.extend(simplefan(obstacleList,waypointList[i],waypointList[i+1],width,height))
		else:
			overallPath.extend(extendingfan(obstacleList, waypointList[i], waypointList[i + 1],width,height))
	return overallPath

#this is a simple path planner I came up with on the fly without too much thought put into it
def simplefan(obstacleList, startpos, endpos, width, height):
    segmentLength = 10
    currentpos = startpos
    segments = []
    for i in range(1000): #loop forever until the end condition is met
        bestscore = 0 #initialize best score
        bestpos = currentpos #initialize best position
        for theta in range(0, math.floor((2*math.pi)*100)): #fan through 0 to 2pi
            testpos = Position(currentpos.x + segmentLength * math.cos(theta/100), currentpos.y + segmentLength * math.sin(theta/100)) #test a position at that angle
            if testpos.within(0, 0, width, height): #if the test position is within the bounds of the field
                testfitness = 1/testpos.distanceTo(endpos) #the fitness is equal to 1 over the distance (shorter distance, higher score)
                
                #if the test position is inside of an object, assign it a score of 0 so it doesn't get picked
                for obstacle in obstacleList: 
                    dist = obstacle.distanceTo(testpos)
                    if dist-10 < 0:
                        testfitness = 0
                        break
                testfitness /= testpos.distanceTo(endpos)

                #if this test position had the highest fitness score out of all the previous test positions, record it
                if testfitness > bestscore:
                    bestpos = testpos
                    bestscore = testfitness
                    
        #set the current position to the best scoring test position, append it to the path array.
        segments.append(Segment(currentpos, bestpos))      
        currentpos = bestpos
        
        #if we're close enough, call it quits
        if currentpos.distanceTo(endpos) < 10:
            break
    return segments
            
#this works the same as the simple fan, but extends the segment length to try to reach the end goal in less moves and detect obstacles earlier.
def extendingfan(obstacleList, startpos, endpos, width, height):
	currentpos = startpos
	segments = []
	for i in range(100):
		bestscore = 0 #initialize best score
		bestpos = currentpos #initialize best position
		for theta in range(0, math.floor((2*math.pi)*100)): #fan through 0 to 2pi
			usable = True #boolean to keep track of whether the extending segment goes through an obstacle
			for segmentLength in range(1, 15):
				testpos = Position(currentpos.x + segmentLength * 15 * math.cos(theta/100), currentpos.y + segmentLength * 15 * math.sin(theta/100))
				if testpos.within(0, 0, width, height): #if the test position is within the bounds of the field
					testfitness = 1/testpos.distanceTo(endpos) #the fitness is equal to 1 over the distance (shorter distance, higher score)

					#if the test position is inside of an object, assign it a score of 0 so it doesn't get picked
					for obstacle in obstacleList: 
						dist = obstacle.distanceTo(testpos)
						if dist-10 < 0:
							usable = False
							break
					testfitness /= testpos.distanceTo(endpos)

					#if this test position had the highest fitness score out of all the previous test positions, record it
					if testfitness > bestscore and usable:
						bestpos = testpos
						bestscore = testfitness
                    
        #set the current position to the best scoring test position, append it to the path array.
		segments.append(Segment(currentpos, bestpos))      
		currentpos = bestpos

		#if we're close enough, call it quits
		if currentpos.distanceTo(endpos) < 10:
			break
	return segments
				
                
