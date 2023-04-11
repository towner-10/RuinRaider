from pygame import Rect
from src.lib.node import Node, neighbors
from src.math.a_star import algorithm, get_closest_node

def print_grid_with_path(nodes, path):
    for col in nodes:
        for node in col:
            # If the node is in the path, print a *
            if node in path:
                print("*", end=" ")
            # If the node is not active, print a -
            elif not node.active:
                print("#", end=" ")
            # If the node is active, print a .
            else:
                print(".", end=" ")
        print()

# Test neighbors
def test_neighbors():
    # Create a 2D array of rects
    rects = [[Rect(x * 10, y * 10, 10, 10) for x in range(10)] for y in range(10)]

    # Create a 2D array of nodes from the rects
    nodes = [[Node(rect) for rect in col] for col in rects]

    # Get neighbors for each node
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):
            nodes[i][j].neighbors = neighbors(nodes, i, j)

    # Assert that the first node has 3 neighbors
    assert len(nodes[0][0].neighbors) == 3

    # Assert that the last node has 3 neighbors
    assert len(nodes[9][9].neighbors) == 3

    # Assert that the middle node has 8 neighbors
    assert len(nodes[5][5].neighbors) == 8

# Test get_closest_node
def test_get_closest_node():
    # Create a 2D array of rects
    rects = [[Rect(x * 10, y * 10, 10, 10) for x in range(10)] for y in range(10)]

    # Create a 2D array of nodes from the rects
    nodes = [[Node(rect) for rect in col] for col in rects]

    # Get the closest node to the current position
    closest_node = get_closest_node(nodes, (0, 0))

    # Assert that the closest node is not None
    assert closest_node is not None

    # Assert that the closest node is the first node in the 2D array
    assert closest_node == nodes[0][0]

# Test A* pathfinding
def test_astar():
    # Create a 2D array of rects
    rects = [[Rect(x * 10, y * 10, 10, 10) for x in range(10)] for y in range(10)]

    # Create a 2D array of nodes from the rects
    nodes = [[Node(rect) for rect in col] for col in rects]

    # Set middle nodes to inactive
    for i in range(1, 9):
        for j in range(1, 9):
            nodes[i][j].active = False

    # Get neighbors for each node
    for i in range(len(nodes)):
        for j in range(len(nodes[i])):
            nodes[i][j].neighbors = neighbors(nodes, i, j)

    # Set the start and end nodes
    start_node = nodes[0][0]
    end_node = nodes[9][9]

    # Get the path
    path = algorithm(nodes, (start_node.x, start_node.y), (end_node.x, end_node.y))

    # Print the grid with the path
    print()
    print("Grid of Nodes with Path:")
    print_grid_with_path(nodes, path)
    print()

    # Assert that the path is not empty
    assert path

    # Assert that the start node is in the path
    assert start_node in path

    # Assert that the end node is in the path
    assert end_node in path

    # Assert that the start node is the first node in the path
    assert path[0] == start_node

    # Assert that the end node is the last node in the path
    assert path[-1] == end_node

    # Assert that the path is the correct length
    assert len(path) == 18
