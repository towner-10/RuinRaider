import numpy as np
from src.lib.node import Node, get_closest_node

def algorithm(
    nodes: list[list[Node]],
    current_pos: tuple[int, int],
    target_pos: tuple[int, int],
) -> list[Node]:
    current_node = get_closest_node(nodes, current_pos)
    target_node = get_closest_node(nodes, target_pos)

    # Clear the connections
    for col in nodes:
        for node in col:
            node.connection = None

    # If the current node is the target node, return the current node
    if current_node == target_node:
        return [current_node]

    # Set the current node's g value to 0
    current_node.set_g(0)

    # Set the current node's h value to the distance between the current node and the target node
    current_node.set_h(np.sqrt((current_node.x - target_node.x) ** 2 + (current_node.y - target_node.y) ** 2))

    # Create a list of open nodes and a list of closed nodes
    toSearch = set([current_node])
    searched = set()

    # Loop through the open nodes
    while len(toSearch) > 0:
        current_node = min(toSearch, key=lambda node: node.get_f())

        if current_node == target_node:
            path = [current_node]

            # Loop through the connections
            while current_node.connection is not None:
                # Add the connection to the path
                path.append(current_node.connection)

                # Set the current node to the connection
                current_node = current_node.connection

            # Reverse the path and return it
            return path[::-1]

        # Remove the current node from the open nodes list and add it to the closed nodes list
        toSearch.remove(current_node)
        searched.add(current_node)

        for neighbor in current_node.neighbors:
            in_search = neighbor in toSearch

            # If the neighbor is not active or the neighbor is in the closed nodes list, skip it
            if not neighbor.active or neighbor in searched:
                continue

            cost_dist = np.sqrt((neighbor.x - current_node.x) ** 2 + (neighbor.y - current_node.y) ** 2)
            cost_to_neighbor = current_node.get_g() + cost_dist

            # If the neighbor is not in the open nodes list, set the neighbor's g value to the cost to the neighbor and add it to the open nodes list
            if not in_search or cost_to_neighbor < neighbor.get_g():
                neighbor.set_g(cost_to_neighbor)
                neighbor.connection = current_node

                if not in_search:
                    h_dist = np.sqrt((neighbor.x - target_node.x) ** 2 + (neighbor.y - target_node.y) ** 2)
                    neighbor.set_h(h_dist)
                    toSearch.add(neighbor)

    return []