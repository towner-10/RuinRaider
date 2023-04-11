import pygame

from src.lib.tilemap import TiledMap
from src.lib.node import Node, neighbors

class Navmesh:
    def __init__(self, size: tuple[int, int], tile_size: int, tilemap: TiledMap, collidable_layers: tuple[str]):
        self.size = size
        self.tile_size = tile_size
        self.__nodes = self.generate(tilemap, collidable_layers)
        self.__time = 0

        # Generate the neighbors for each node
        for i in range(len(self.__nodes)):
            for j in range(len(self.__nodes[i])):
                self.__nodes[i][j].neighbors = neighbors(self.__nodes, i, j)

    @property
    def nodes(self):
        return self.__nodes 
    
    # Calculate the next time the A* algorithm should be run
    def update(self):
        """Update the navmesh. This should be called once every 1000 ms."""
        if self.__time < pygame.time.get_ticks():
            self.__time = pygame.time.get_ticks() + 500

    def should_update(self) -> bool:
        return pygame.time.get_ticks() > self.__time

    def generate(self, tilemap: TiledMap, layers: tuple[str]) -> list[list[Node]]:
        """Generate a navmesh from a tilemap."""
        navmesh: list[list[Node]] = []

        # Find rectangles that are collidable
        rects = []
        for layer in layers:
            rects.extend(tilemap.get_rects_in_layer(layer))

        for y in range(0, self.size[1], self.tile_size):
            row = []
            for x in range(0, self.size[0], self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                active = True
                for r in rects:
                    if r.colliderect(rect):
                        active = False
                        break
                row.append(Node(rect, active))
            navmesh.append(row)

        return navmesh
    
    def debug_render(self, surface: pygame.Surface, color: tuple[int, int, int] = (255, 0, 0), active_color: tuple[int, int, int] = (0, 255, 0)):
        """Render the navmesh for debugging purposes."""
        for row in self.__nodes:
            for node in row:
                if node.active:
                    pygame.draw.rect(surface, active_color, node.get(pygame.Rect), 1)
                else:
                    pygame.draw.rect(surface, color, node.get(pygame.Rect), 1)

    def debug_render_line_of_nodes(self, surface: pygame.Surface, nodes: list[Node], color: tuple[int, int, int] = (255, 0, 0)):
        """Render a line of nodes for debugging purposes."""
        for i in range(len(nodes) - 1):
            pygame.draw.line(surface, color, nodes[i].get(pygame.Rect).center, nodes[i + 1].get(pygame.Rect).center, 1)
