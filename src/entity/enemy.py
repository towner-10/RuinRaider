from pygame import image, Rect
from pygame.math import Vector2

from src.lib.node import Node
from src.lib.transform import Transform
from src.entity.character import Character


# Enemy class for spiders and crawlers
class Enemy(Character):
    def __init__(self, position:Vector2 = Vector2(0,0), hp=100, speed=2, is_spider=False):
        # Get proper enemy sprite
        if not is_spider:
            img_path='assets\sprites\crawler\crawler_walk.png'
        else:
            img_path='assets\sprites\spider\spider.png'

        super().__init__(image.load(img_path), position, 270)
        self.hp = hp
        self.speed = speed
        self.damage = 20
        self.direction = Vector2(0,0)
        self.__nodes: list[Node] = []
        self.is_spider = is_spider
    
    # Method called from weapon classes to damage enemy
    def hit(self, weapon_damage):
        self.hp -= weapon_damage

    # Methods for pathfinding
    def get_nodes(self):
        return self.__nodes
    def set_nodes(self, nodes):
        self.__nodes = nodes

    # Pathfinding movement
    def update(self):
        if len(self.__nodes) > 0:
            current_node_vector = Vector2(self.__nodes[0].get(Rect).centerx, self.__nodes[0].get(Rect).centery)
            self.direction: Vector2 = current_node_vector - self.get(Transform).pos
            if self.direction.length() == 0:
                self.direction = Vector2(0,0)
            else:
                self.direction = self.direction.normalize()
            self.move(self.direction * self.speed)

            # Remove node if reached
            if self.get(Transform).pos.distance_to(current_node_vector) < 32:
                self.__nodes.pop(0)

    def render(self, screen):
        # Rotate in direction of movement
        self.rotate(-self.direction.as_polar()[1])

        # Render in screen
        super().render(screen)
