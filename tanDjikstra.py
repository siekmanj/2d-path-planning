'''
This is the algorithm that will path plan around the boundary of the flight zone as well as around all of the obstacles
in the field using a circular tangent based approach
'''

from nodes import *
from obstacle import *
from boundingSegment import *


def initialize_nodes(waypoint_list,obstacle_list,bound_segments):
    # This function will initialize all of the nodes for the djikstra path planning
    # In future, support will be added for multiple waypoints, for now, just between two.
    # For now it will just return all of the straight segments in between the tangent segments

    nodes = []

    #start node(Can be simulated as an obstacle with a radius of 0)
    startNode = ObstacleNode(Obstacle(waypoint_list[0],0),1,0)
    startNode.type = 0
    startNode.pathDistance = 0
    nodes.append(startNode)


    #Add all of the concave vertices.
    vertexPos, connectedSegs = getConcaveVertices(bound_segments)
    nodes.extend(posToObstacleNodes(vertexPos,connectedSegs))

    obsNumber = 0
    #Add all of the obstacles to the position nodes
    for obs in obstacle_list:
        obsNumber += 1
        nodes.append(ObstacleNode(obs,1,obsNumber))
        nodes.append(ObstacleNode(obs,-1,obsNumber))

    endNode = ObstacleNode(Obstacle(waypoint_list[1], 0), 1,0)
    endNode.type = 0
    nodes.append(endNode)

    return nodes

def getConcaveVertices(bound_segments):
    # This is a function that will iterate through all of the boundary vertices of the flight zone and will figure out which ones
    # are concave vertices that could be used as nodes

    concaveVertices = []
    connectedSegs = []
    for i in range(0,len(bound_segments)):
        # Iterate through all of the bound segments to figure out whether or not they are concave.
        prev_point = bound_segments[i-1].startPos
        current_point = bound_segments[i].startPos
        next_point = bound_segments[i].endPos

        temp_segments = bound_segments[:]

        # Delete the previous current and previous segments so that a new one can be added
        del temp_segments[i]
        del temp_segments[i-1]

        temp_segments.append(BoundSegment(prev_point,next_point))

        if current_point.inBounds(temp_segments):
            concaveVertices.append(current_point)
            connectedSegs.append([i,i-1])
    #This returns the positions of the concave vertices in a list with another 2d array with the a pair of indices for
    #each corresponding to which bounding segments can be ignored when going through all of the
    #print(connectedSegs)
    return concaveVertices,connectedSegs


def posToObstacleNodes(positions,connectedSegs):
    # This is a function that will take a given position and convert it into an obstacle with radius 0 that can be used as a node
    obstacleNodes = []

    for i in range(0,len(positions)):
        obstacle = Obstacle(positions[i],0)
        obsNode = ObstacleNode(obstacle,1,-1,connectedSegs[i])
        obstacleNodes.append(obsNode)

    return obstacleNodes

def nodesToPath(nodes):
    #This function will take the nodes in and will then calculate smaller segmented paths.

    #How many segments per one cotangent segment
    numSegsPerStraight = 4
    numAngleStepsPerCircle = 500
    approximateAngleStep = 2*math.pi/numAngleStepsPerCircle

    path = []

    # Append all of the segments to the path
    currentNode = len(nodes) - 1
    # path = []
    while currentNode != 0:
        currentSegment = nodes[currentNode].segmentIn
        startX = currentSegment.startPos.x
        startY = currentSegment.startPos.y
        endX = currentSegment.endPos.x
        endY = currentSegment.endPos.y

        #Change in x,y between each of the spaced out segments
        dx = (endX-startX)/(numSegsPerStraight)
        dy = (endY-startY)/(numSegsPerStraight)

        #Split up the current segment into numSegsPerStraight
        for i in range(0,numSegsPerStraight):
            #Create the current segment
            smallerStart = Position(endX-dx*(i+1),endY-dy*(i+1))
            smallerEnd = Position(endX-dx*i,endY-dy*i)

            smallerSegment = Segment(smallerStart,smallerEnd)

            path.append(smallerSegment)

        parentNode = nodes[nodes[currentNode].parent]
        #Add the curvy part of the segment
        if parentNode.type > 0:
            #The curvy part will need to be added

            dx = parentNode.segmentIn.endPos.x - parentNode.position.x
            dy = parentNode.segmentIn.endPos.y - parentNode.position.y
            parentNode.firstAngle = math.atan2(dy, dx)

            dx = nodes[currentNode].segmentIn.startPos.x - parentNode.position.x
            dy = nodes[currentNode].segmentIn.startPos.y - parentNode.position.y
            parentNode.secondAngle = math.atan2(dy, dx)

            #All of the angles should be normalized between 0 and 2pi
            if parentNode.firstAngle < 0:
                parentNode.firstAngle += 2 * math.pi
            elif parentNode.firstAngle > 2 * math.pi:
                parentNode.firstAngle -= 2 * math.pi

            if parentNode.secondAngle < 0:
                parentNode.secondAngle += 2 * math.pi
            elif parentNode.secondAngle > 2 * math.pi:
                parentNode.secondAngle -= 2 * math.pi

            #Direection 1 = CCW(+ angles) -1 = CW(- angles)
            if parentNode.direction == 1:
                #If the direction is CCW
                if parentNode.secondAngle < parentNode.firstAngle:
                    #If the second angle is smaller make it bigger so that the angle can be correctly calculated
                    parentNode.secondAngle = parentNode.secondAngle + math.pi*2


            elif parentNode.direction == -1:
                if parentNode.secondAngle > parentNode.firstAngle:
                    parentNode.secondAngle = parentNode.secondAngle - math.pi*2

            angle_diff = parentNode.secondAngle - parentNode.firstAngle
            numRadiusSegments = abs(math.floor(angle_diff / approximateAngleStep))
            angleStep = angle_diff / numRadiusSegments

            #Loop to actually create the segments
            for i in range(0,numRadiusSegments):
                #Create the current start and finish x and y values for the individual arc segment
                startAngle = parentNode.secondAngle - angleStep * (i+1)
                endAngle = parentNode.secondAngle - angleStep * i
                radStartX = parentNode.position.x + parentNode.radius*math.cos(startAngle)
                radStartY = parentNode.position.y + parentNode.radius*math.sin(startAngle)
                radEndX = parentNode.position.x + parentNode.radius*math.cos(endAngle)
                radEndY = parentNode.position.y + parentNode.radius*math.sin(endAngle)
                radStartPos = Position(radStartX,radStartY)
                radEndPos = Position(radEndX,radEndY)
                radSegment = Segment(radStartPos,radEndPos)
                path.append(radSegment)




        currentNode = nodes[currentNode].parent

    return path


def tangentDjikstra(waypoint_list,obstacle_list,bound_segements):

    nodes = initialize_nodes(waypoint_list,obstacle_list,bound_segements)

    # Iterate through the process until the final node is known
    allpath = []
    nonintersectingpath =[]
    while not nodes[-1].known:
        # find the minimum distance from the list
        id, minDisNode = min((enum for enum in enumerate(nodes) if not enum[1].known) , key = lambda x: x[1].pathDistance)
        #print('Id Value')
        #print(id)
        nodes[id].known = True
        #if nodes[id].type != 0 and id != 0:
        #    #Set the first angle of the node
        #    segment = nodes[nodes[id].parent].getCoTanSeg(nodes[id])
        #    dx = segment.startPos.x - nodes[id].position.x
        #    dy = segment.startPos.y - nodes[id].position.y

        #    nodes[id].firstAngle = customMath.getAngleFromX(dx,dy)

        # Iterate through all of the other nodes
        for i in range(0,len(nodes)):
            #print('I value')
            #print(i)
            # Conditions not to check the node
            #print('id')
            #print(id)
            #print('direction')
            #print(minDisNode.direction)
            if nodes[i].known:
                #print('passed known')
                pass
            elif (i == id + minDisNode.direction) and minDisNode.type != 0:
                #print('passed same obs')
                pass
            else:
                #print('run through')
                # Calculate the distance to the node from the current node
                #print(minDisNode.position.x)
                #print(minDisNode.position.y)
                #print(i)
                #print(nodes[i].position.x)
                #print(nodes[i].position.y)
                # First calculate the cotangent segment between the two nodes
                coTanSeg = minDisNode.getCoTanSeg(nodes[i])
                allpath.append(coTanSeg)

                # Check whether or not there is an intersection
                # Make a list of all of the obstacles that need to be checked
                obsToCheck = obstacle_list[:]
                indToDel = []
                if nodes[i].type > 0:
                    indToDel.append(nodes[i].type - 1)
                    #print('howdy')
                    #print(nodes[i].type)
                if minDisNode.type > 0:
                    #print('hi')
                    #print(minDisNode.type)
                    indToDel.append(minDisNode.type - 1)

                indToDel.sort(reverse = True)

                #print(indToDel)
                #print(len(obstacle_list))
                #Delete all of those obstacles from the obsToCheck list
                for j in indToDel:
                    del obsToCheck[j]

                ignoreSegs = None
                if minDisNode.type == -1:
                    ignoreSegs = minDisNode.ignoreSegs
                elif nodes[i].type == -1:
                    ignoreSegs = nodes[i].ignoreSegs
                lineIntersection = coTanSeg.getIntersecting(obsToCheck,bound_segements,ignoreSegs)
                circleIntersection = minDisNode.getCircleIntersection(obsToCheck)

                if (not lineIntersection) and (not circleIntersection):

                    nonintersectingpath.append(coTanSeg)
                    if minDisNode.type == 0 or minDisNode.type == -1:#If it is either of the point types tell the program that it does not eed to use the arc distance
                        possibleDistance = minDisNode.getDistanceTo(nodes[i],False)
                    else:
                        possibleDistance = minDisNode.getDistanceTo(nodes[i],True)

                    #Check if this distance is less than the previous distance.
                    if possibleDistance < nodes[i].pathDistance:
                        nodes[i].pathDistance = possibleDistance
                        nodes[i].parent = id
                        nodes[i].segmentIn = coTanSeg
                        if minDisNode.type == 0 or minDisNode.type == -1:
                            minDisNode.direction = nodes[i].direction
                            dx = nodes[i].segmentIn.endPos.x - nodes[i].position.x
                            dy = nodes[i].segmentIn.endPos.y - nodes[i].position.y
                            nodes[i].firstAngle = math.atan2(dy,dx)
                        elif minDisNode.direction == nodes[i].direction:
                            nodes[i].firstAngle = minDisNode.secondAngle
                        else:
                            nodes[i].firstAngle = minDisNode.secondAngle+math.pi

    path = nodesToPath(nodes)

    return path,allpath,nonintersectingpath
