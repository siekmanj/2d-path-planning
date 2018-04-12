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
    vertexPos = getConcaveVertices(bound_segments)
    nodes.extend(posToObstacleNodes(vertexPos))

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

    return concaveVertices


def posToObstacleNodes(positions):
    # This is a function that will take a given position and convert it into an obstacle with radius 0 that can be used as a node
    obstacleNodes = []

    for pos in positions:
        obstacle = Obstacle(pos,0)
        obsNode = ObstacleNode(obstacle,1,0)
        obstacleNodes.append(obsNode)

    return obstacleNodes

def tangentDjikstra(waypoint_list,obstacle_list,bound_segements):

    nodes = initialize_nodes(waypoint_list,obstacle_list,bound_segements)

    # Iterate through the process until the final node is known
    path = []
    allpath = []
    workpath =[]
    while not nodes[-1].known:
        # find the minimum distance from the list
        id, minDisNode = min((enum for enum in enumerate(nodes) if not enum[1].known) , key = lambda x: x[1].pathDistance)
        #print('Id Value')
        #print(id)
        nodes[id].known = True
        if nodes[id].type != 0 and id != 0:
            #Set the first angle of the node
            segment = nodes[nodes[id].parent].getCoTanSeg(nodes[id])
            dx = segment.startPos.x - nodes[id].position.x
            dy = segment.startPos.y - nodes[id].position.y

            nodes[id].firstAngle = customMath.getAngleFromX(dx,dy)

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
                if nodes[i].type != 0:
                    indToDel.append(nodes[i].type - 1)
                    #print('howdy')
                    #print(nodes[i].type)
                if minDisNode.type != 0:
                    #print('hi')
                    #print(minDisNode.type)
                    indToDel.append(minDisNode.type - 1)

                indToDel.sort(reverse = True)

                #print(indToDel)
                #print(len(obstacle_list))
                #Delete all of those obstacles from the obsToCheck list
                for j in indToDel:
                    del obsToCheck[j]

                lineIntersection = coTanSeg.getIntersecting(obsToCheck,bound_segements)
                circleIntersection = minDisNode.getCircleIntersection(obsToCheck)

                if (not lineIntersection) and (not circleIntersection):

                    workpath.append(coTanSeg)
                    if minDisNode.type == 0:
                        possibleDistance = minDisNode.getDistanceTo(nodes[i],False)
                    else:
                        possibleDistance = minDisNode.getDistanceTo(nodes[i],True)

                    #Check if this distance is less than the previous distance.
                    if possibleDistance < nodes[i].pathDistance:
                        nodes[i].pathDistance = possibleDistance
                        nodes[i].parent = id
                        nodes[i].segmentIn = coTanSeg
                        if minDisNode.type == 0:
                            minDisNode.direction = nodes[i].direction
                        if minDisNode.direction == nodes[i].direction:
                            nodes[i].firstAngle = minDisNode.secondAngle
                        else:
                            nodes[i].firstAngle = minDisNode.secondAngle+math.pi
                else:
                    print('\nrejected\n')
                    if minDisNode.type == 0:
                        print('Point')
                    else:
                        print('Circle')
                    print(' to ')
                    if nodes[i].type == 0:
                        print('Point')
                    else:
                        print('Circle')
                    print('\nbecause of:  ')
                    print('\n')
    #Append all of the segments to the path
    currentNode = len(nodes) - 1
    #path = []
    while currentNode != 0:
        path.append(nodes[currentNode].segmentIn)
        currentNode = nodes[currentNode].parent

    return path,allpath,workpath