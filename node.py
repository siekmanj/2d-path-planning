import position
import math

class Node:
	def __init__(self, position):
		self.position = position
        self.prev_node = self
        self.

    def setPreviousNode(self, prev_node):
        self.prev_node = prev_node

	def distanceToPreviousNode(self):
		return math.sqrt(math.pow(self.position.x - self.prev_node.position.x, 2) + math.pow(self.position.y - self.prev_node.position.y, 2))
