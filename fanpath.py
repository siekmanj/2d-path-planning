from position import *
import math
import random

#this is a simple path planner I came up with on the fly without too much thought put into it
def simplefan(obstacleList, startpos, endpos):
    segmentLength = 10 
    currentpos = startpos
    path = []
    while True: #loop forever until the end condition is met
        bestscore = 0 #initialize best score
        bestpos = currentpos #initialize best position
        for theta in range(0, math.floor((2*math.pi)*100)): #fan through 0 to 2pi
            testpos = Position(currentpos.x + segmentLength * math.cos(theta/100), currentpos.y + segmentLength * math.sin(theta/100)) #test a position at that angle
            if testpos.within(0, 0, 1000, 600): #if the test position is within the bounds of the field
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
        currentpos = bestpos
        path.append(currentpos)      
        
        #if we're close enough, call it quits
        if currentpos.distanceTo(endpos) < 10:
            break
    return path
            
                