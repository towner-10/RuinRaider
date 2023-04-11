from pygame.math import Vector2
from pygame import Surface, image

from src.lib.sprite import Sprite
from src.lib.transform import Transform
from src.entity.entity import Entity

# Class to manage crystal objects
class Crystal(Entity):
    def __init__(self, x):
        super().__init__(
            Transform(Vector2(x, 350), 0, 57,57),
            Sprite(image.load('assets/sprites/arctbeast/projectile.png'))
            )
        self.direction = Vector2(0, 1)
        self.speed = 8
        self.damage = 200
        self.get(Sprite).set_rect(self.get(Transform).pos)

    # Render crystal to screen
    def render(self, screen: Surface):
        self.get(Sprite).render(screen)

    # Reverse crystal direction when hit by bullet
    def reverse(self):
        self.speed *= -1

    # Update rect and move crystal
    def update(self):
        self.get(Sprite).rect = self.get(Transform).get_hitbox()
        self.get(Transform).pos += self.direction * self.speed