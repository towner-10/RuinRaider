import numpy as np
import pygame
from src.entity.entity import Entity

class Node(Entity):
    """A node is a point in the grid that can be connected to other nodes."""
    def __init__(self, rect: pygame.Rect, active: bool = True):
        """Create a new node."""
        super().__init__(rect)
        self.x = rect.x
        self.y = rect.y
        self.active = active
        self.neighbors: list[Node] = []
        self.connection: Node = None
        self.__g: float = 0.0
        self.__h: float = 0.0

    def get_f(self):
        """Get the f value of the node."""
        return self.__g + self.__h

    def set_g(self, value: float):
        """Set the g value of the node."""
        self.__g = value

    def get_g(self):
        """Get the g value of the node."""
        return self.__g

    def set_h(self, value: float):
        """Set the h value of the node."""
        self.__h = value

    def get_h(self):
        """Get the h value of the node."""
        return self.__h
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"Node({self.get(pygame.Rect).center}, {self.active})"
    
    def __eq__(self, other):
        return self.get(pygame.Rect).center == other.get(pygame.Rect).center

    def __repr__(self):
        return str(self)


def get_closest_node(nodes: list[Node], pos: tuple[int, int]) -> Node | None:
    """Get the closest node to the current position"""
    closest_node = None
    closest_distance = 0

    # Loop through 2D array of nodes
    for col in nodes:
        for node in col:
            # If the node is not active, skip it
            if not node.active:
                continue

            # Get the distance between the current position and the node position
            distance = np.sqrt((node.x - pos[0]) ** 2 + (node.y - pos[1]) ** 2)

            # If the closest node is None, set it to the current node
            if closest_node is None:
                closest_node = node
                closest_distance = distance

            # If the distance is less than the closest distance, set it to the current node
            elif distance < closest_distance:
                closest_node = node
                closest_distance = distance

    return closest_node

def neighbors(nodes: list[list[Node]], rowNumber: int, colNumber: int) -> list[Node]:
    """Generate the neighbors for each node"""
    neighbors = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if rowNumber + i >= 0 and rowNumber + i < len(nodes):
                if colNumber + j >= 0 and colNumber + j < len(nodes[rowNumber + i]):
                    if nodes[rowNumber + i][colNumber + j].active:
                        neighbors.append(nodes[rowNumber + i][colNumber + j])

    return neighbors