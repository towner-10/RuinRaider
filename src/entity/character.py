from pygame import Surface
from pygame.math import Vector2

from src.entity.entity import Entity
from src.lib.transform import Transform
from src.lib.sprite import Sprite

# Base class for moving entities 
class Character(Entity):
    def __init__(self, sprite: Surface, position: Vector2 = Vector2(0,0), angle: float=0):
        super().__init__(
            Transform(position, angle, 32, 32),
            Sprite(sprite),
        )
        
        # Resizing character sprite if necessary
        self.get(Sprite).scale(self.get(Transform).width, self.get(Transform).height)
        self.get(Sprite).set_rect(self.get(Transform).pos)

        # Vector to track direction of movement
        self.direction = Vector2(0,0)

    # Rotating the sprite and object 
    def rotate(self, angle):
        self.get(Transform).angle = angle
        self.get(Sprite).rotate(angle)

    # Rotating towards a specific position
    def rotate_towards(self, pos: Vector2):
        direction = pos - self.get(Transform).pos
        radius, angle = direction.as_polar()
        self.rotate(-angle)

    # Moving the character
    def move(self, vector):
        self.get(Transform).pos += vector
        self.get(Sprite).move(self.get(Transform).pos)    

    # Getting rect for collisions
    def get_hitbox(self):
        return self.get(Transform).get_hitbox()
    
    # Drawing the character
    def render(self, screen):
        sprite = self.get(Sprite)
        sprite.render(screen)


