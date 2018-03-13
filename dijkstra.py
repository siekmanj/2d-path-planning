from position import Position
from segment import Segment
from node import Node
import math
import random

#TODO: FINISH
def shortestPath(obstacles, waypoints, FIELD_HEIGHT, FIELD_WIDTH):
	#Each x,y coord is a node
	unvisited = []
	open = []
	for x in range(0, FIELD_WIDTH, 20):
		for y in range(0, FIELD_HEIGHT, 20):
			unvisited.append(Position(x, y))

	initial = unvisited[0]
